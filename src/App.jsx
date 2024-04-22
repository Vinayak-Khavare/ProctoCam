import { Link } from "react-router-dom";
import { Navbar } from "./components/Navbar";

function App() {
  return (
    <>
      <Navbar />
      <section>
        <div className="grid min-h-[89vh]">
          <div className="place-self-center">
            <p className="px-5 lato-black text-6xl max-[787px]:text-4xl text-center leading-tight">
              <span className="glow">
                Empower Your Exam and Interview <br /> Performance with
                ProctoCam
              </span>
            </p>
            <div className="flex max-[787px]:block max-[787px]:px-5 space-x-3 max-[787px]:space-x-0 max-[787px]:space-y-3 justify-center mt-6">
              <Link
                to="/candidate"
                className="btn btn-wide btn-lg max-[787px]:btn-block btn-primary font-bold"
              >
                Try As Student
              </Link>
              <Link
                to="/admin"
                className="btn btn-wide btn-lg max-[787px]:btn-block btn-secondary font-bold"
              >
                Try As Admin
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default App;
