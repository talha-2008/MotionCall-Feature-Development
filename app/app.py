import reflex as rx
from app.states.state import State
from app.states.room_state import RoomState


def topbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon(tag="video", class_name="w-6 h-6 text-indigo-400"),
                rx.el.h1("MotionCall", class_name="text-2xl font-bold text-white"),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.p(
                    f"Room: {RoomState.current_room_name}",
                    class_name="text-sm text-gray-400 font-medium",
                ),
                class_name="hidden md:flex items-center gap-4",
            ),
            rx.el.div(
                rx.icon(
                    tag="settings",
                    class_name="w-6 h-6 text-gray-400 hover:text-white transition-colors cursor-pointer",
                ),
                rx.icon(
                    tag="user",
                    class_name="w-6 h-6 text-gray-400 hover:text-white transition-colors cursor-pointer",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between w-full h-full px-4 md:px-6",
        ),
        class_name="h-16 w-full bg-[#151a21] border-b border-gray-700 fixed top-0 left-0 z-50",
    )


def video_tile(id: str, name: str) -> rx.Component:
    return rx.el.div(
        rx.el.video(
            id=id,
            class_name="w-full h-full bg-black object-cover",
            auto_play=True,
            muted=True if id == "localVideo" else False,
            plays_inline=True,
        ),
        rx.el.p(
            name,
            class_name="absolute bottom-2 left-2 text-sm font-medium text-white bg-black/50 px-2 py-1 rounded",
        ),
        class_name="aspect-video bg-gray-800 rounded-lg overflow-hidden relative shadow-lg",
    )


def call_controls() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon(
                tag=rx.cond(RoomState.is_mic_on, "mic", "mic-off"), class_name="w-5 h-5"
            ),
            on_click=RoomState.toggle_mic,
            class_name=rx.cond(
                RoomState.is_mic_on,
                "bg-gray-700 hover:bg-gray-600",
                "bg-red-500 hover:bg-red-600",
            )
            + " p-3 rounded-full text-white transition-colors",
        ),
        rx.el.button(
            rx.icon(
                tag=rx.cond(RoomState.is_video_on, "video", "video-off"),
                class_name="w-5 h-5",
            ),
            on_click=RoomState.toggle_video,
            class_name=rx.cond(
                RoomState.is_video_on,
                "bg-gray-700 hover:bg-gray-600",
                "bg-red-500 hover:bg-red-600",
            )
            + " p-3 rounded-full text-white transition-colors",
        ),
        rx.el.button(
            rx.icon(tag="screen-share", class_name="w-5 h-5"),
            on_click=RoomState.toggle_screen_share,
            class_name="p-3 rounded-full text-white transition-colors "
            + rx.cond(
                RoomState.is_screen_sharing,
                "bg-indigo-600 hover:bg-indigo-700",
                "bg-gray-700 hover:bg-gray-600",
            ),
        ),
        rx.el.button(
            rx.icon(tag="radio", class_name="w-5 h-5"),
            rx.cond(
                RoomState.is_recording,
                rx.el.span(
                    class_name="animate-ping absolute h-3 w-3 rounded-full bg-red-400 opacity-75 top-0 right-0"
                ),
                rx.fragment(),
            ),
            on_click=RoomState.toggle_recording,
            class_name="relative p-3 rounded-full text-white transition-colors "
            + rx.cond(
                RoomState.is_recording,
                "bg-red-500 hover:bg-red-600",
                "bg-gray-700 hover:bg-gray-600",
            ),
        ),
        rx.el.a(
            rx.icon(tag="phone-off", class_name="w-5 h-5"),
            href="/",
            class_name="p-3 bg-red-500 rounded-full text-white hover:bg-red-600 transition-colors",
        ),
        class_name="flex items-center justify-center gap-4",
    )


def chat_message(message: dict) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            rx.el.span(f"{message['sender']}: ", class_name="font-semibold"),
            message["text"],
        ),
        class_name="text-sm text-white",
    )


def chat_panel() -> rx.Component:
    return rx.el.div(
        rx.el.h3("চ্যাট", class_name="text-lg font-semibold text-white mb-4"),
        rx.el.div(
            rx.foreach(RoomState.messages, chat_message),
            class_name="flex-grow mb-4 space-y-2 overflow-y-auto",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.input(
                    placeholder="বার্তা পাঠান...",
                    name="chat_message",
                    class_name="w-full bg-gray-700 border-gray-600 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500",
                    default_value=RoomState.current_message,
                ),
                rx.el.button(
                    rx.icon(tag="send", class_name="w-5 h-5"),
                    type="submit",
                    class_name="p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors",
                ),
                class_name="flex gap-2",
            ),
            on_submit=RoomState.send_chat_message,
            reset_on_submit=True,
            class_name="mt-auto",
        ),
        class_name="flex flex-col h-full",
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    tag="video", class_name="w-16 h-16 text-indigo-400 mx-auto mb-4"
                ),
                rx.el.h1(
                    "MotionCall", class_name="text-5xl font-bold text-white text-center"
                ),
                rx.el.p(
                    "सरल, शक्तिशाली, এবং সুরক্ষিত ভিডিও কল।",
                    class_name="text-lg text-gray-400 mt-4 text-center",
                ),
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.input(
                        placeholder="কক্ষের নাম লিখুন",
                        name="room_name",
                        class_name="w-full h-12 px-4 bg-[#151a21] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-shadow",
                        size="3",
                    ),
                    rx.el.button(
                        "যোগ দিন",
                        rx.icon(tag="arrow_right", class_name="ml-2"),
                        type="submit",
                        class_name="h-12 px-8 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors flex items-center justify-center",
                        size="3",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-[1fr,auto] gap-4 w-full max-w-lg",
                ),
                on_submit=State.join_room,
                class_name="mt-12 flex justify-center",
            ),
            class_name="flex flex-col items-center justify-center text-center w-full",
        ),
        class_name="font-['Inter'] bg-[#0f1216] text-white min-h-screen flex items-center justify-center p-4",
    )


def room() -> rx.Component:
    return rx.el.main(
        topbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    video_tile(id="localVideo", name="You"),
                    video_tile(id="remoteVideo", name="Peer"),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 flex-grow p-4",
                ),
                rx.el.div(
                    call_controls(),
                    class_name="w-full py-4 bg-[#151a21] border-t border-gray-700",
                ),
                class_name="flex flex-col flex-grow",
            ),
            rx.el.div(
                chat_panel(),
                class_name="w-full md:w-80 lg:w-96 bg-[#151a21] border-l border-gray-700 p-4 h-full hidden md:flex flex-col",
            ),
            class_name="flex flex-col md:flex-row h-screen pt-16",
        ),
        class_name="font-['Inter'] bg-[#0f1216] text-white min-h-screen",
        on_mount=RoomState.on_room_load,
        on_unmount=rx.call_script("webrtc.leave()"),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(src="/webrtc.js"),
        rx.el.script(src="/room.js"),
    ],
)
app.add_page(index)
app.add_page(room, route="/room/[room_name]")