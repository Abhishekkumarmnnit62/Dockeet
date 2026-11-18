import { useState } from "react";

import DocumentPanel from "./components/DocumentPanel";
import ChatPanel from "./components/ChatPanel";
//import ObservationPanel from "./components/ObservationPanel";

function App() {

  const [
    selectedDocument,
    setSelectedDocument
  ] = useState("all");

  const [
    observations,
    setObservations
  ] = useState(null);

  return (

    <div className="app-layout">

      <DocumentPanel
        selectedDocument={selectedDocument}
        setSelectedDocument={setSelectedDocument}
      />

      <ChatPanel
        selectedDocument={selectedDocument}
        setObservations={setObservations}
      />

      

    </div>

  );
}

export default App;