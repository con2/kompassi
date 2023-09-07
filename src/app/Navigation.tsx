"use client";

import Link from "next/link";
import { detectedLanguage, setLanguage, t } from "../translations";
import { useCallback } from "react";

const Navigation = () => {
  const otherLanguageCode = detectedLanguage == "en" ? "fi" : "en";
  const otherLanguageName = t((r) => r.LanguageSelection[otherLanguageCode]);
  const toggleLanguage = useCallback(
    () => setLanguage(otherLanguageCode),
    [otherLanguageCode]
  );
  return (
    <div className="navbar navbar-dark bg-primary navbar-expand-lg">
      <div className="container-fluid">
        <Link href="/" className="navbar-brand">{t((r) => r.Brand.appName)}</Link>
          <div className="navbar-nav ms-auto">
            <a href="" onClick={toggleLanguage}>{otherLanguageName}</a>
          </div>
      </div>
    </div>
  );
};

export default Navigation;
