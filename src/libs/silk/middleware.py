import traceback

from django.db.models.sql.compiler import SQLInsertCompiler
from django.utils import timezone
from django.utils.encoding import force_str
from silk.collector import DataCollector
from silk.middleware import SilkyMiddleware as OriginalSilkyMiddleware
from silk.profiling.profiler import silk_meta_profiler
# this is not a good approach to rely on internal methods of a third-party library because such details can
# be changed in other versions without notifying clients
from silk.sql import _should_wrap


# this function was inspired by the execute_sql function from the silk.sql module and adjusted for processing
# insert queries
def execute_insert_sql(self, *args, **kwargs):
    """wrapper around real execute_sql in order to extract information"""
    should_wrap = False
    insert_sql_queries = []
    # collect all insert statements in case of bulk operation because _execute_sql method runs all queries at once
    for q, params in self.as_sql():
        sql_query_compiled = q % tuple(force_str(param) for param in params)
        insert_sql_queries.append(sql_query_compiled)
        should_wrap = should_wrap or _should_wrap(sql_query_compiled)  # if at least one query should be tracked, track the entire batch

    if should_wrap:
        tb = ''.join(reversed(traceback.format_stack()))
        query_dict = {
            'query': "\n\n".join(insert_sql_queries),  # preserve all insert statements in case of bulk operation
            'start_time': timezone.now(),
            'traceback': tb
        }
        try:
            return self._execute_sql(*args, **kwargs)
        finally:
            query_dict['end_time'] = timezone.now()
            request = DataCollector().request
            if request:
                query_dict['request'] = request
            if getattr(self.query.model, '__module__', '') != 'silk.models':
                # since the EXPLAIN operation runs a query, insert statements may lead to creating additional rows or
                # raising unique constraint violation, so this was removed from here
                DataCollector().register_query(query_dict)
            else:
                DataCollector().register_silk_query(query_dict)
    return self._execute_sql(*args, **kwargs)


class SilkyMiddleware(OriginalSilkyMiddleware):
    @silk_meta_profiler()
    def process_request(self, request):
        super().process_request(request)

        # this flag is set up in the parent's method
        if getattr(request, 'silk_is_intercepted', False):
            # the original Silky middleware checks like this if not hasattr(SQLCompiler, '_execute_sql')
            # this cannot be applied here because SQLInsertCompiler inherits SQLCompiler, thus it inherits _execute_sql
            # method, so we need a check which would be unique to the SQLInsertCompiler class
            if not getattr(SQLInsertCompiler, '_silk_patched', False):
                SQLInsertCompiler._silk_patched = True
                SQLInsertCompiler._execute_sql = SQLInsertCompiler.execute_sql
                SQLInsertCompiler.execute_sql = execute_insert_sql
