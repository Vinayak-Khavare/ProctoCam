import { useEffect, useRef, useState } from "react";
import { ThemeButton } from "../components/ThemeButton";
import io from "socket.io-client";

export default function Candidate() {
  const socket = io("http://127.0.0.1:5000");
  const [messages, setMessages] = useState([]);
  const warningModal = useRef(null);
  const videoCameraPreview = useRef(null);

  const stopVideoStream = () => {
    if (videoCameraPreview.current && videoCameraPreview.current.srcObject) {
      const tracks = videoCameraPreview.current.srcObject.getTracks();
      tracks.forEach((track) => track.stop());
      videoCameraPreview.current.srcObject = null;
      console.log("video off");
    }
  };

  useEffect(() => {
    async function streamVideo() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        videoCameraPreview.current.srcObject = stream;
      } catch (err) {
        console.error("Error accessing the webcam: ", err);
      }
    }
    streamVideo();
    socket.on("connect", () => {
      socket.emit("connect", { message: "Client Connected." });
    });

    // warningModal.current.showModal();
    socket.on("cheating_detected", (data) => {
      console.log("Warning: ", data.message);
      warningModal.current.showModal();

      setMessages((messages) => [
        ...messages,
        { name: data.name, text: data.message },
      ]);
    });

    return () => {
      socket.disconnect();
      stopVideoStream();
    };
  }, []);

  return (
    <div>
      <dialog ref={warningModal} id="warning-modal" className="modal">
        <div className="modal-box w-11/12 max-w-5xl bg-warning text-warning-content">
          <h3 className="font-bold text-lg">Warning!</h3>
          <p className="py-4">
            It seems like you are cheating in this session. If you repeat such
            activity then this session will get terminated.
          </p>
          <div className="modal-action">
            <form method="dialog">
              {/* if there is a button, it will close the modal */}
              <button className="btn btn-secondary">Close</button>
            </form>
          </div>
        </div>
      </dialog>

      <video
        className="fixed right-2 bottom-2 z-20 w-[256px] h-[144px] bg-gray-600 rounded-xl"
        ref={videoCameraPreview}
        autoPlay
      ></video>

      <div className="bg-base-200 grid grid-cols-4">
        <aside className="col-span-1 min-h-screen bg-base-300 px-4">
          <div className="lato-black text-2xl accent-content py-4">
            Messages
          </div>
          <div className="flex flex-col justify-between h-[88%]">
            <div className="overflow-y-scroll no-scrollbar h-[80%]">
              {messages.map((message, index) => {
                if (message.name === "admin") {
                  return (
                    <div key={index} class="chat chat-start">
                      <div class="chat-bubble">{message.text}</div>
                    </div>
                  );
                }
              })}

              {/* <div class="chat chat-end"> */}
              {/*   <div class="chat-bubble">You underestimate my power!</div> */}
              {/* </div> */}
            </div>
            {/* <div className="flex gap-2"> */}
            {/*   <input */}
            {/*     type="text" */}
            {/*     placeholder="Type here" */}
            {/*     className="input input-bordered w-full max-w-xs" */}
            {/*   /> */}
            {/*   <a className="btn btn-accent text-accent-content">Send</a> */}
            {/* </div> */}
          </div>
        </aside>
        <div className="col-span-3">
          <div className="navbar">
            <div className="flex-1">
              <a className="btn btn-lg lato-bold">Hello, Candidate 👋</a>
            </div>
            <div className="flex-none">
              <ThemeButton className="btn btn-ghost justify-self-end" />
            </div>
          </div>
          <div className="flex flex-col gap-5 h-auto items-center justify-center mt-5">
            {/* <video */}

            <div className="flex gap-3 justify-center"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
