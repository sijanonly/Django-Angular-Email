from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import (
    MessageSerializer, MessagePostSerializer
)

from .models import Message


class MessageMixin(object):
    """
    Mixin to inherit from.
    Here we're setting the query set and the serializer
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        This view should return a list of sections.
        """
        return Message.objects.filter(
            receivers__id__in=[self.request.user.id]
        )


class MessageList(MessageMixin, generics.ListCreateAPIView):

    """
    Return a list of all the messages, or
    create new ones
    """
    pass


class SentMesssageList(generics.ListAPIView):
    """
    Return sent message list
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        This view should return a list of all sections by messages.
        """
        # program_slug = self.kwargs.get('program_slug')
        # return Section.objects.filter(
        #     program__slug=program_slug
        # )
        sent_messages = Message.objects.filter(sender__id=self.request.user.id)
        receivers = []
        for each_message in sent_messages:
            for receiver in each_message.receivers.all():
                receivers.append(receiver.id)
        return Message.objects.filter(sender__id=self.request.user.id)


class MessagePost(generics.CreateAPIView):
    model = Message
    serializer_class = MessagePostSerializer

    def post(self, request, *args, **kwargs):
        receivers = request.data.get('receiver', None)
        total_receivers = []
        msg_header = ''
        msg_content = ''
        if receivers is None or len(receivers) == 0:
            programs = request.data.pop('programs')
            grades = []
            grade_recievers = []
            sections_code = []
            sections_receivers = []
            for each_program in programs:
                sections = programs[each_program]['sections']
                for section in sections:
                    is_grade_selected = section.get('selected', False)
                    if is_grade_selected:
                        grades.append(section['id'])
                    else:
                        grade_sections = section.get('grade_sections')
                        for each_section in grade_sections:
                            is_section_selected =\
                                each_section.get('selected', False)
                            if is_section_selected:
                                sections_code.append(each_section['code'])
            for each_grade in grades:
                students = Student.objects.filter(section__grade=each_grade)
                for each_student in students:
                    grade_recievers.append(
                        each_student.entrance_application.user.id)
            for each_section in sections_receivers:
                students = Student.objects.filter(section__cod=each_section)
                for each_student in students:
                    sections_receivers.append(
                        each_student.entrance_application.user.id)

            # total_receivers = grade_recievers + sections_receivers + [request.user.id]
            total_receivers = grade_recievers + sections_receivers
            # for test example data
            # total_receivers = [21, 22]
            msg_header = request.data['msg_header_bulk']
            msg_content = request.data['msg_content_bulk']
        else:
            for each_receiver in receivers:
                total_receivers.append(each_receiver['id'])
            msg_header = request.data['msg_header']
            msg_content = request.data['msg_content']
        sender = request.user.id
        data = {
            'sender': sender,
            'receivers': total_receivers,
            'msg_header': msg_header,
            'msg_content': msg_content
        }
        serializer = MessagePostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # if notification:
            #     notification.send(
            #         [request.user],
            #         "email_sent",
            #         {"from_user": request.user})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)