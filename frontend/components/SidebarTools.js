"use client";
import React from "react";

import ModelSelector from "./ModelSelector";
import QADBManager from "./QADBManager";
import ContextManager from "./ContextManager";

export default function SidebarTools() {
  return (
    <>
      <ModelSelector />
      <QADBManager />
      <ContextManager />
    </>
  );
}
