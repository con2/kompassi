import graphene

from ..models.enums import MessageApp, MessageDispatch, MessageState

MessageAppType = graphene.Enum.from_enum(MessageApp)
MessageDispatchType = graphene.Enum.from_enum(MessageDispatch)
MessageStateType = graphene.Enum.from_enum(MessageState)
