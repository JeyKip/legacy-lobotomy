from .models import (PlaybookAssignment, PlaybookTextBlock,
                     PlaybookAssignmentBlock, PlaybookImageBlock,
                     PlaybookVideoBlock, PlaybookQuestionBlock, PlaybookOption)

from assignments.models import (AssignmentBlock, TextBlock, ImageBlock,
                                VideoBlock, QuestionBlock, Option)


def create_playbook_assignment(user, assignment):
    depend = None
    if assignment.dependent_on:
        depend = PlaybookAssignment.objects.filter(name=assignment.dependent_on).first()

    playbook_assignment = PlaybookAssignment.objects.create(
        user=user,
        name=assignment.name,
        description=assignment.description,
        image=assignment.image,
        points=assignment.points,
        time=assignment.time,
        category=assignment.category,
        priority=assignment.priority,
        dependent_on=depend
    )

    for assignment_block in AssignmentBlock.objects.filter(
            assignment_id=assignment.id):
        playbook_assignment_block = PlaybookAssignmentBlock.objects.create(
            name=assignment_block.name,
            type_of_block=assignment_block.type_of_block,
            assignment=playbook_assignment
        )
        for text_block in TextBlock.objects.filter(
                block_id=assignment_block.id):
            PlaybookTextBlock.objects.create(
                block=playbook_assignment_block,
                text=text_block.text
            )
        for image_block in ImageBlock.objects.filter(
                block_id=assignment_block.id):
            PlaybookImageBlock.objects.create(
                block=playbook_assignment_block,
                image=image_block.image
            )
        for video_block in VideoBlock.objects.filter(
                block_id=assignment_block.id):
            PlaybookVideoBlock.objects.create(
                block=playbook_assignment_block,
                video=video_block.video
            )
        for question_block in QuestionBlock.objects.filter(
                block_id=assignment_block.id):
            playbook_question_block = PlaybookQuestionBlock.objects.create(
                block=playbook_assignment_block,
                text=question_block.text
            )
            for option in Option.objects.filter(question_id=question_block.id):
                PlaybookOption.objects.create(
                    text=option.text,
                    tip=option.tip,
                    is_correct=option.is_correct,
                    question=playbook_question_block
                )
