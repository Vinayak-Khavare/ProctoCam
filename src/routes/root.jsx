import { useEffect, useRef } from "react";
import { ThemeButton } from "../components/ThemeButton";

export default function Root() {
  const videoCameraPreview = useRef({});

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
  }, []);
  return (
    <div>
      <div className="bg-base-200 grid grid-cols-4">
        <aside className="col-span-1 min-h-screen bg-base-300 px-4">
          <div className="lato-black text-2xl accent-content py-4">
            Messages
          </div>
          <div className="h-full">
            <div className="overflow-y-scroll m">hello</div>
            <div className="flex gap-2 ">
              <input
                type="text"
                placeholder="Type here"
                className="input input-bordered w-full max-w-xs"
              />
              <a className="btn btn-primary">Send</a>
            </div>
          </div>
        </aside>
        <div className="col-span-3">
          <div className="navbar">
            <div className="flex-1">
              <a className="btn btn-lg lato-bold">Hello, username👋</a>
            </div>
            <div className="flex-none">
              <ThemeButton className="btn btn-ghost justify-self-end" />
            </div>
          </div>
          <div className="flex flex-col gap-5 h-auto items-center justify-center mt-5">
            <video
              className="bg-gray-900 rounded-3xl ring ring-base-content w-[40rem] h-[22.5rem]"
              ref={videoCameraPreview}
              autoPlay
            ></video>
            <div className="flex gap-3 justify-center">
              <a className="btn btn-warning">Send Warning</a>
              <a className="btn btn-accent">End Session</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
