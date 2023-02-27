from rest_framework.request import Request

from rooms.selectors.selector_v1_room import RoomSelector
from wishlists.models.wish_list import Wishlist


class WishlistService:
    def __init__(self, request: Request) -> None:
        self.request = request

    def toggle_wish_list(self, room_id: int) -> None:
        wishlist = Wishlist.objects.filter(user=self.request.user).first()

        if wishlist is None:
            wishlist = Wishlist.objects.create(
                user=self.request.user, name=f"{self.request.user.name} 님의 찜 목록"
            )
        room_selector = RoomSelector(self.request)
        room = room_selector.get_room(room_id)
        if wishlist.rooms.filter(pk=room_id).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
