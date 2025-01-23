import { useEffect, useRef } from "react";
import { ThemeButton } from "../components/ThemeButton";
import { useNavigate } from "react-router-dom";
import VideoCamera from "../components/VideoCamera";

export default function Admin() {
  const navigate = useNavigate();

  useEffect(() => {
    return () => {
      console.log("unmounted");
    };
  }, []);

  const handleBackNavigation = () => {
    stopVideoStream();
    navigate(-1); // Navigate back in history
  };

  return (
    <div>
      <div className="bg-base-200 grid grid-cols-4">
        <aside className="col-span-1 min-h-screen bg-base-300 px-4">
          <div className="lato-black text-2xl accent-content py-4">
            Messages
          </div>
          <div className="flex flex-col justify-between h-[88%]">
            <div className="overflow-y-scroll no-scrollbar h-[80%]">
              <div className="chat chat-start">
                <div className="chat-bubble">
                  It's over Anakin, <br />I have the high ground.
                </div>
              </div>
              <div className="chat chat-end">
                <div className="chat-bubble">You underestimate my power!</div>
              </div>
            </div>
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
            <VideoCamera />
            <div className="flex gap-3 justify-center">
              <button className="btn btn-warning">Send Warning</button>
              <button onClick={handleBackNavigation} className="btn btn-accent">
                End Session
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
