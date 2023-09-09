import datetime
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def create_file_name_with_timestamp(basename):
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    name_with_timestamp = "_".join([basename, suffix])
    return name_with_timestamp


def get_final_name(filename, name_timestamp):
    name, ext = get_filename_ext(filename)
    return '{new_filename}{ext}'.format(new_filename=name_timestamp, ext=ext)


def upload_image_path(instance, filename):
    name_with_timestamp = create_file_name_with_timestamp('image')
    final_name = get_final_name(filename, name_with_timestamp)
    return 'assignments/images/{final_name}'.format(final_name=final_name)


def upload_video_path(instance, filename):
    name_with_timestamp = create_file_name_with_timestamp('video')
    final_name = get_final_name(filename, name_with_timestamp)
    return 'assignments/videos/{final_name}'.format(final_name=final_name)


def upload_file_path(instance, filename):
    name_with_timestamp = create_file_name_with_timestamp('file')
    final_name = get_final_name(filename, name_with_timestamp)
    return 'assignments/files/{final_name}'.format(final_name=final_name)


content_types = ('video/mpg', 'video/mp2', 'video/mpeg',
                 'video/mpe', 'video/mpv', 'video/mp4',
                 'video/m4p', 'video/m4v', 'video/qt',
                 'video/mov', 'video/wmv', 'video/flv',
                 'video/avi', 'video/mkv', 'video/quicktime')
