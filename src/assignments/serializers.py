from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import (Assignment, Category, Option, QuestionBlock, TextBlock,
                     ImageBlock, VideoBlock, AssignmentBlock)

from .models import UserAssignment
from users.models import User

from playbooks.models import PlaybookAssignment


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class TextBlockSerializer(ModelSerializer):
    class Meta:
        model = TextBlock
        fields = '__all__'


class ImageBlockSerializer(ModelSerializer):
    class Meta:
        model = ImageBlock
        fields = '__all__'


class VideoBlockSerializer(ModelSerializer):
    class Meta:
        model = VideoBlock
        fields = '__all__'


class QuestionBlockSerializer(ModelSerializer):
    class Meta:
        model = QuestionBlock
        fields = '__all__'

    options = OptionSerializer(many=True, read_only=True)


class AssignmentBlockSerializer(ModelSerializer):
    class Meta:
        model = AssignmentBlock
        fields = '__all__'

    text = TextBlockSerializer(read_only=True)
    image = ImageBlockSerializer(read_only=True)
    video = VideoBlockSerializer(read_only=True)
    question = QuestionBlockSerializer(read_only=True)


class AssingmentSerializer(ModelSerializer):
    blocks = SerializerMethodField()
    locked = SerializerMethodField()
    dependent_on_name = SerializerMethodField()
    category = SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_dependent_on_name(self, obj):
        if obj.dependent_on:
            assignment = Assignment.objects.filter(id=obj.dependent_on.id).first()
            if assignment:
                return assignment.name

    def get_category(self, obj):
        category = Category.objects.get(id=obj.category.id)
        return CategorySerializer(category, many=False).data

    def get_locked(self, obj):
        request = self.context.get('request', None)
        if request:
            user = request.user
            userassignment = UserAssignment.objects.get(assignment_id=obj.id,
                                                        user=user)
            return userassignment.locked()

    def get_blocks(self, instance):
        blocks = instance.blocks.all().order_by('id')
        return AssignmentBlockSerializer(blocks, many=True).data


class PlaybookAssignmentsSerializer(AssingmentSerializer):
    is_completed = SerializerMethodField(source='get_is_completed')

    def get_is_completed(self, obj):
        return True


class UserPlaybookSerializer(ModelSerializer):
    assignments = SerializerMethodField(source='get_assignments')
    points = SerializerMethodField(source='get_points')

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'age', 'points', 'activity',
            'assignments')

    def get_assignments_queryset(self, user):
        queryset = PlaybookAssignment.objects.filter(
            user=user
        ).order_by('-completed')
        return queryset

    def get_assignments(self, obj):
        assignments = []
        assignments_queryset = self.get_assignments_queryset(user=obj)
        for assignment_queryset in assignments_queryset:
            assignments.append(AssingmentSerializer(assignment_queryset).data)
        return assignments

    def get_points(self, obj):
        assignments_queryset = self.get_assignments_queryset(user=obj)
        points = []
        for assignment_queryset in assignments_queryset:
            points.append(
                AssingmentSerializer(assignment_queryset).data['points'])
        return sum(points)
