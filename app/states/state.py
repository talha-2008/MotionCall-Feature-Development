import reflex as rx


class State(rx.State):
    """The base state for the app."""

    def join_room(self, form_data: dict[str, str]):
        """Redirects to the room page."""
        room_name = form_data.get("room_name")
        if room_name:
            return rx.redirect(f"/room/{room_name.lower().strip()}")