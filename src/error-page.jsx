import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <div
      data-theme="sunset"
      className="bg-base-100 min-h-screen grid place-content-center"
    >
      <div className="text-center space-y-3">
        <h1 className="lato-black text-7xl">Oops!</h1>
        <p className="lato-bold text-lg">
          Sorry, an unexpected error has occurred.
        </p>
        <p className="text-base-content/35">
          <i>{error.statusText || error.message}</i>
        </p>
      </div>
    </div>
  );
}
