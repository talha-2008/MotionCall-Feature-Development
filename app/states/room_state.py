import reflex as rx
from typing import Any


class RoomState(rx.State):
    """State for the video call room."""

    is_mic_on: bool = True
    is_video_on: bool = True
    is_screen_sharing: bool = False
    is_recording: bool = False
    messages: list[dict[str, str]] = []
    current_message: str = ""

    @rx.var
    def current_room_name(self) -> str:
        """Get the room name from the URL."""
        return self.router.page.params.get("room_name", "unknown")

    def on_room_load(self):
        room_name = self.current_room_name
        return rx.call_script(f'room.join("{room_name}")')

    def toggle_mic(self):
        self.is_mic_on = not self.is_mic_on
        return rx.call_script(f"webrtc.toggleAudio({str(self.is_mic_on).lower()})")

    def toggle_video(self):
        self.is_video_on = not self.is_video_on
        return rx.call_script(f"webrtc.toggleVideo({str(self.is_video_on).lower()})")

    def toggle_screen_share(self):
        self.is_screen_sharing = not self.is_screen_sharing
        return rx.call_script("webrtc.toggleScreenShare()")

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        return rx.call_script("webrtc.toggleRecording()")

    @rx.event
    def send_offer(self, offer: dict):
        return rx.call_script(f'room.handle_signal({{"offer": {offer}}})')

    @rx.event
    def send_answer(self, answer: dict):
        return rx.call_script(f'room.handle_signal({{"answer": {answer}}})')

    @rx.event
    def send_ice_candidate(self, candidate: dict):
        return rx.call_script(f'room.handle_signal({{"iceCandidate": {candidate}}})')

    @rx.event
    def remote_peer_online(self, _):
        return rx.call_script("webrtc.sendOffer()")

    def send_chat_message(self, form_data: dict[str, str]):
        message = form_data.get("chat_message", "")
        if not message.strip():
            return
        message_data = {"sender": "You", "text": message}
        self.messages.append(message_data)
        yield rx.call_script(f'webrtc.sendChatMessage("{message}")')
        self.current_message = ""

    @rx.event
    def receive_chat_message(self, message: str):
        message_data = {"sender": "Peer", "text": message}
        self.messages.append(message_data)