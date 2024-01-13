import { ReactNode } from "react";
import { Layout } from "./models";

interface SubmitButtonProps {
  layout?: Layout;
  children?: ReactNode;
}

export default function SubmitButton({ layout, children }: SubmitButtonProps) {
  switch (layout) {
    case Layout.Horizontal:
      return (
        <div className="row mb-3">
          <div className="col-md-3"></div>
          <div className="col-md-9">
            <button type="submit" className="btn btn-primary">
              {children}
            </button>
          </div>
        </div>
      );
    default:
      return (
        <button type="submit" className="btn btn-primary mb-3">
          {children}
        </button>
      );
  }
}
