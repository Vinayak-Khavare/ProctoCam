import { Navbar } from "./components/Navbar";

function App() {
  return (
    <>
      <Navbar />
      <section>
        <div className="grid min-h-[89vh]">
          <div className="place-self-center">
            <p className="px-5 lato-black text-6xl max-[787px]:text-4xl text-center leading-tight bg-gradient-to-tr from-cyan-500 via-pink-500 to-yellow-600 bg-clip-text text-transparent">
              Empower Your Exam and Interview <br /> Performance with ProctoCam
            </p>
            <div className="flex max-[787px]:block max-[787px]:px-5 space-x-3 max-[787px]:space-x-0 max-[787px]:space-y-3 justify-center mt-6">
              <a className="btn btn-wide btn-lg max-[787px]:btn-block btn-primary font-bold">
                Try As Student
              </a>
              <a className="btn btn-wide btn-lg max-[787px]:btn-block btn-secondary font-bold">
                Try As Admin
              </a>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default App;
