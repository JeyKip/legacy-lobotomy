import codecs
import csv
import mimetypes
import os
import pathlib
import urllib

import requests
from django.core.files import File

from .models import Assignment, Category, AssingmentTarget, AssignmentBlock, TextBlock, QuestionBlock, Option, \
    ImageBlock, VideoBlock


def check_csv_file(csv_file):
    error = False
    error_message = None
    extension = pathlib.Path(csv_file.name).suffix
    if extension != '.csv':
        error = True
        error_message = 'Selected file is not csv. Please select valid csv file'

    return error, error_message


def get_assignments_from_file(csv_file):
    the_file = csv_file.open('rb')
    assignments = csv.DictReader(
        codecs.iterdecode(the_file, 'utf-8'), delimiter=',')
    assignments_dict = []
    for assignment in assignments:
        assignments_dict.append(assignment)
    return assignments_dict


def check_and_create_assignments(assignments):
    error, error_message = check_assignments(assignments)
    if not error:
        create_assignments(assignments)
    return error, error_message


def check_assignments(assignments):
    mandatory_fields = get_mandatory_fields()
    error = False
    error_message = None
    for row, assignment_dict in enumerate(assignments):
        for mandatory_field in mandatory_fields:
            if not assignment_dict.get(mandatory_field) \
                    or assignment_dict.get(mandatory_field) == '':
                error = True
                error_message = \
                    f'Row {row + 1} has an error. Missing {mandatory_field} field.' \
                    f'Please check your csv file.'
                return error, error_message
            elif mandatory_field == 'name':
                error, error_message = check_name(assignment_dict, row)
                if error:
                    return error, error_message
            elif mandatory_field == 'tile_image':
                error, error_message = check_image_link(assignment_dict, 'tile_image', row)
                if error:
                    return error, error_message
            elif mandatory_field == 'category':
                error, error_message = check_category(assignment_dict, row)
                if error:
                    return error, error_message
            elif mandatory_field == 'target':
                error, error_message = check_target(assignment_dict, row)
                if error:
                    return error, error_message
            elif mandatory_field == 'points' or mandatory_field == 'priority':
                error, error_message = check_points_or_priority(
                    assignment_dict=assignment_dict,
                    mandatory_field=mandatory_field,
                    row=row
                )
                if error:
                    return error, error_message
        if (assignment_dict.get('time') or assignment_dict.get('time') != '') \
                and not (assignment_dict.get('time')).isnumeric():
            error = True
            error_message = \
                f'Row {row + 1} has an error. Field time must be whole number. ' \
                f'Please check your csv file.'
            return error, error_message
        elif assignment_dict.get('dependent_on') is not None \
                and assignment_dict.get('dependent_on') != '':
            if assignment_dict.get('dependent_on') == assignment_dict.get('name'):
                error = True
                error_message = \
                    f'Row {row + 1} has an error. ' \
                    f'Assignment cannot be dependent on itself. ' \
                    f'Please check your csv file.'
                return error, error_message
        error, error_message = check_block_assignment(row, assignment_dict)
        if error:
            return error, error_message
    return error, error_message


def check_name(assignment_dict, row):
    error = False
    error_message = None
    assignment_name = assignment_dict.get('name')
    if Assignment.objects.filter(name=assignment_name):
        error = True
        error_message = \
            f'Row {row + 1} has an error. Assignment {assignment_name} already exist. ' \
            f'Please check your csv file.'
    return error, error_message


def check_image_link(assignment_dict, header, row):
    error = False
    error_message = None
    image_url = assignment_dict.get(header)
    headers = requests.head(image_url).headers
    content_type = headers.get('Content-Type')
    # size = int(headers.get('Content-Length'))
    image_formats = ['image/bmp', 'image/gif', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/tiff',
                     'image/webp']
    if content_type not in image_formats:
        error = True
        error_message = \
            f'Row {row + 1} has an error. Image link in {header} is not correct. ' \
            f'Please check your csv file.'

    return error, error_message


def check_category(assignment_dict, row):
    error = False
    error_message = None
    category_name = assignment_dict.get('category')
    if not Category.objects.filter(name=category_name):
        error = True
        error_message = \
            f'Row {row + 1} has an error. Category {category_name} not exist. ' \
            f'Please check your csv file.'
    return error, error_message


def check_target(assignment_dict, row):
    error = False
    error_message = None
    target_name = assignment_dict.get('target')
    if not AssingmentTarget.objects.filter(name=target_name):
        error = True
        error_message = \
            f'Row {row + 1} has an error. Assignment target {target_name} not exist. ' \
            f'Please check your csv file.'
    return error, error_message


def check_points_or_priority(assignment_dict, mandatory_field, row):
    error = False
    error_message = None
    field_value = assignment_dict.get(mandatory_field)
    if not field_value.isnumeric():
        error = True
        error_message = \
            f'Row {row + 1} has an error. Field {mandatory_field} must be whole number. ' \
            f'Please check your csv file.'
    return error, error_message


def check_block_assignment(row, assignment):
    error = False
    error_message = None
    for index, header in enumerate(assignment.keys()):
        if not error:
            try:
                if 'block_type' in header:
                    if 'block' not in (list(assignment.keys()))[index + 1]:
                        error, error_message = block_error_message(row, header)
                    elif assignment.get(header) == 'Image':
                        error, error_message = check_image_link(
                            assignment_dict=assignment,
                            header=(list(assignment.keys()))[index + 1],
                            row=row)
                    elif assignment.get(header) == 'Video':
                        error, error_message = check_video_link(
                            assignment_dict=assignment,
                            header=(list(assignment.keys()))[index + 1],
                            row=row)
                    elif assignment.get(header) == 'Question':
                        error, error_message = check_options_in_question(row, index, assignment)
            except IndexError:
                error, error_message = block_error_message(row, header)
        else:
            return error, error_message
    return error, error_message


def block_error_message(row, header):
    error = True
    error_message = \
        f'Row {row + 1} has an error. Block header {header} is incomplete. ' \
        f'Please check your csv file.'
    return error, error_message


def check_video_link(assignment_dict, header, row):
    error = False
    error_message = None
    video_url = assignment_dict.get(header)
    headers = requests.head(video_url).headers
    content_type = headers.get('Content-Type')
    # size = int(headers.get('Content-Length'))
    video_formats = ['video/3gpp', 'video/mp4', 'video/mpeg', 'video/ogg',
                     'video/quicktime', 'video/webm', 'video/x-m4v', 'video/ms-asf',
                     'video/x-ms-wmv', 'video/x-msvideo']
    if content_type not in video_formats:
        error = True
        error_message = \
            f'Row {row + 1} has an error. Video link in {header} is not correct. ' \
            f'Please check your csv file.'

    return error, error_message


def check_options_in_question(row, index, assignment):
    error = False
    error_message = None
    index_for_option_correct = index + 4
    option_is_correct_exist = False
    try:
        while 'option' in (list(assignment.keys()))[index_for_option_correct]:
            if assignment.get((list(assignment.keys()))[index_for_option_correct]) == 'true':
                if not option_is_correct_exist:
                    option_is_correct_exist = True
                else:
                    error = True
                    error_message = \
                        f'Row {row + 1} has an error. More than one option is correct ' \
                        f'Please check your csv file.'
                    return error, error_message
            index_for_option_correct += 3
    except IndexError:
        return error, error_message
    return error, error_message


def get_mandatory_fields():
    return [
        'name',
        'description',
        'tile_image',
        'points',
        'priority',
        'category',
        'target'
    ]


def create_assignments(assignments):
    for assignment_dict in assignments:
        tile_image = download_file(file_url=assignment_dict.get('tile_image'))
        time = assignment_dict.get('time')
        category = Category.objects.get(name=assignment_dict.get('category'))
        target = AssingmentTarget.objects.get(name=assignment_dict.get('target'))
        dependent_on = Assignment.objects.filter(
            name=assignment_dict.get('dependent_on')).first()
        if time == '':
            time = None
        assignment_obj = Assignment.objects.create(
            name=assignment_dict.get('name'),
            description=assignment_dict.get('description'),
            image=tile_image,
            points=assignment_dict.get('points'),
            time=time,
            priority=assignment_dict.get('priority'),
            category=category,
            target=target,
            dependent_on=dependent_on
        )

        delete_file(tile_image.name)
        create_blocks_for_assignment(assignment_obj=assignment_obj,
                                     assignment_dict=assignment_dict)


def download_file(file_url):
    response = requests.get(file_url)
    content_type = response.headers.get('Content-Type')
    extension = mimetypes.guess_extension(content_type)
    file_name = f'temp_file{extension}'

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    with urllib.request.urlopen(file_url) as response, \
            open(file_name, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

    new_file = File(open(file_name, "rb"))

    return new_file


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


def create_blocks_for_assignment(assignment_obj, assignment_dict):
    for index, header in enumerate(assignment_dict.keys()):
        if 'block_type' in header:
            if assignment_dict.get(header) == 'Text':
                create_text_block(
                    assignment_obj=assignment_obj,
                    block_content=assignment_dict.get(
                        (list(assignment_dict.keys()))[index + 1])
                )
            elif assignment_dict.get(header) == 'Image':
                create_image_block(
                    assignment_obj=assignment_obj,
                    image_url=assignment_dict.get(
                        (list(assignment_dict.keys()))[index + 1])
                )
            elif assignment_dict.get(header) == 'Video':
                create_video_block(
                    assignment_obj=assignment_obj,
                    video_url=assignment_dict.get(
                        (list(assignment_dict.keys()))[index + 1])
                )
            elif assignment_dict.get(header) == 'Question':
                question_content = get_question_content(index, assignment_dict)
                create_question_block(assignment_obj=assignment_obj,
                                      question_content=question_content)


def create_text_block(assignment_obj, block_content):
    assignment_block_obj = create_assignment_block(assignment_obj, 'Text')
    TextBlock.objects.create(
        block=assignment_block_obj,
        text=block_content)


def create_image_block(assignment_obj, image_url):
    assignment_block_obj = create_assignment_block(assignment_obj, 'Image')
    image = download_file(file_url=image_url)
    ImageBlock.objects.create(
        block=assignment_block_obj,
        image=image)

    delete_file(image.name)


def create_video_block(assignment_obj, video_url):
    assignment_block_obj = create_assignment_block(assignment_obj, 'Video')
    image = download_file(file_url=video_url)
    VideoBlock.objects.create(
        block=assignment_block_obj,
        video=image)

    delete_file(image.name)


def create_question_block(assignment_obj, question_content):
    assignment_block_obj = create_assignment_block(assignment_obj, 'Question')
    question_block_obj = QuestionBlock.objects.create(
        block=assignment_block_obj,
        text=question_content.get('question_text')
    )
    question_block_obj.save()
    for option in question_content.get('options'):
        Option.objects.create(
            text=option.get('option_text'),
            tip=option.get('option_tip'),
            is_correct=option.get('option_is_correct'),
            question=question_block_obj
        )


def create_assignment_block(assignment_obj, block_type):
    assignment_block_obj = AssignmentBlock(
        name='BULK_UPLOAD',
        type_of_block=block_type,
        assignment=assignment_obj
    )
    assignment_block_obj.save()
    return assignment_block_obj


def get_question_content(index, assignment_dict):
    options = []
    question = {}
    index_for_question = index
    next_header = (list(assignment_dict.keys()))[index_for_question + 1]
    if 'block' in next_header:
        question_text = assignment_dict.get(next_header)
        option_text = None
        option_tip = None
        option_is_correct = False
        index_for_question += 2
        try:
            while 'option' in (list(assignment_dict.keys()))[index_for_question]:
                if 'option_text' in (list(assignment_dict.keys()))[index_for_question]:
                    option_text = assignment_dict.get((list(assignment_dict.keys()))[index_for_question])
                if 'option_tip' in (list(assignment_dict.keys()))[index_for_question + 1]:
                    option_tip = assignment_dict.get((list(assignment_dict.keys()))[index_for_question + 1])
                if 'option_correct' in (list(assignment_dict.keys()))[index_for_question + 2]:
                    option_is_correct_text = assignment_dict.get(
                        (list(assignment_dict.keys()))[index_for_question + 2])
                    if option_is_correct_text == 'true':
                        option_is_correct = True
                    else:
                        option_is_correct = False
                index_for_question += 3
                option = {
                    'option_text': option_text,
                    'option_tip': option_tip,
                    'option_is_correct': option_is_correct,
                }
                options.append(option)
        except IndexError:
            pass
        question = {
            'question_text': question_text,
            'options': options
        }
    return question
