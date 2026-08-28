import graphene

from ..models.enums import MessageDispatch, MessageState

MessageDispatchType = graphene.Enum.from_enum(MessageDispatch)
MessageStateType = graphene.Enum.from_enum(MessageState)
