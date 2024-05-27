from djchoices import ChoiceItem, DjangoChoices


class FriendRequestStatusChoices(DjangoChoices):
    pending = ChoiceItem("Pending")
    accepted = ChoiceItem("Accepted")
    rejected = ChoiceItem("Rejected")
