import factory

from assignments.models import VideoBlock


class VideoBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoBlock

    # This property must be provided when creating a video block.
    block = None

    # A valid file of the 'video/mpeg' content type with a minimal structure that can be identified as an MPEG video.
    video = factory.django.FileField(
        filename='video.mp4',
        data=b'\x00\x00\x01\xba\x21\x00\x01\x00\x01\x00\x01\x80\x01\x00\x00\x00\x01\xb3\x2c\x01\xe0\x21\x00\x00\x00'
             b'\x00\x01\xb5\x14\x8d\x1b\x16\x10\xff\xff\xc0\x00\x00\x01\xb5\x05\x08\x88\x84\x21\x14\xb6\x03\x21\x32'
             b'\x1f\xff\xfb'
    )
