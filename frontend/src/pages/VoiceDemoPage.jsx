import { useEffect, useMemo, useRef, useState } from "react";

import { api, isMockMode } from "../services/api";
import { tr } from "../services/i18n";

const LANGUAGE_OPTIONS = [
  { value: "en", key: "targetEnglish", fallback: "English" },
  { value: "hi", key: "targetHindi", fallback: "Hindi" },
  { value: "mr", key: "targetMarathi", fallback: "Marathi" },
  { value: "bn", key: "targetBengali", fallback: "Bengali" },
  { value: "ta", key: "targetTamil", fallback: "Tamil" },
  { value: "te", key: "targetTelugu", fallback: "Telugu" },
  { value: "kn", key: "targetKannada", fallback: "Kannada" },
  { value: "or", key: "targetOdia", fallback: "Odia" },
  { value: "ml", key: "targetMalayalam", fallback: "Malayalam" },
];

const DEMO_TEXT = "mujhe seene mein dard ho raha hai aur sans lene mein takleef hai";

function getPreferredMimeType() {
  if (typeof MediaRecorder === "undefined") return "audio/webm";
  if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) return "audio/webm;codecs=opus";
  if (MediaRecorder.isTypeSupported("audio/webm")) return "audio/webm";
  if (MediaRecorder.isTypeSupported("audio/mp4")) return "audio/mp4";
  return "";
}

export default function VoiceDemoPage({ t, language = "en" }) {
  const [audioFile, setAudioFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState("");
  const [transcript, setTranscript] = useState("");
  const [detectedLanguage, setDetectedLanguage] = useState("-");
  const [translatedText, setTranslatedText] = useState("");
  const [targetLanguage, setTargetLanguage] = useState(language === "hi" ? "hi" : "en");
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState("");

  const recorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);

  const supportsRecording = useMemo(
    () => typeof navigator !== "undefined" && !!navigator.mediaDevices?.getUserMedia && typeof MediaRecorder !== "undefined",
    [],
  );

  useEffect(() => {
    setTargetLanguage(language === "hi" ? "hi" : "en");
  }, [language]);

  useEffect(() => {
    return () => {
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
  }, [audioUrl]);

  const stopRecorder = () => {
    if (recorderRef.current && recorderRef.current.state !== "inactive") {
      recorderRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsRecording(false);
  };

  const startRecording = async () => {
    setError("");
    if (!supportsRecording) {
      setError(tr(t, "micNotSupported", "This browser does not support voice recording. Use file upload instead."));
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      chunksRef.current = [];

      const mimeType = getPreferredMimeType();
      const recorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
      recorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      };

      recorder.onstop = () => {
        const type = mimeType || "audio/webm";
        const blob = new Blob(chunksRef.current, { type });
        const file = new File([blob], "voice-input.webm", { type });
        if (audioUrl) URL.revokeObjectURL(audioUrl);
        setAudioFile(file);
        setAudioUrl(URL.createObjectURL(file));
      };

      recorder.start();
      setIsRecording(true);
    } catch {
      setError(tr(t, "micPermissionRequired", "Microphone access is required for voice input."));
      stopRecorder();
    }
  };

  const onSelectFile = (event) => {
    const selected = event.target.files?.[0] || null;
    if (!selected) return;
    setError("");
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioFile(selected);
    setAudioUrl(URL.createObjectURL(selected));
  };

  const transcribe = async () => {
    setError("");
    setIsTranscribing(true);
    try {
      let source = audioFile;
      if (!source && isMockMode()) {
        source = new File([DEMO_TEXT], "mock-voice.txt", { type: "text/plain" });
      }
      if (!source) {
        setError(tr(t, "chooseAudioFile", "Choose Audio File"));
        return;
      }

      const response = await api.transcribeVoice(source);
      setTranscript(response.text || "");
      setDetectedLanguage(response.detected_language || "-");
    } catch (requestError) {
      setError(requestError.message || "Unable to transcribe audio");
    } finally {
      setIsTranscribing(false);
    }
  };

  const translate = async () => {
    setError("");
    if (!transcript.trim()) {
      setError(tr(t, "noTranscriptYet", "No transcript yet."));
      return;
    }

    setIsTranslating(true);
    try {
      const response = await api.processVoice({
        text: transcript,
        target_language: targetLanguage,
      });
      setTranslatedText(response.translated_text || response.text || "");
    } catch (requestError) {
      setError(requestError.message || "Unable to translate transcript");
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <section className="grid-2">
      <article className="panel">
        <h2>{tr(t, "voiceDemoTitle", "BhashaSehat Voice Demo")}</h2>
        <p>{tr(t, "voiceDemoDescription", "Record from microphone or upload an audio file, then transcribe and translate symptoms.")}</p>

        <div className="stack-form">
          <label>{tr(t, "microphone", "Microphone")}</label>
          <button onClick={isRecording ? stopRecorder : startRecording} type="button">
            {isRecording ? tr(t, "stopRecording", "Stop Recording") : tr(t, "startRecording", "Start Recording")}
          </button>
          <small>{isRecording ? tr(t, "micRecording", "Recording...") : tr(t, "micReady", "Ready to record")}</small>

          <label>{tr(t, "chooseAudioFile", "Choose Audio File")}</label>
          <input accept="audio/*" onChange={onSelectFile} type="file" />

          {audioUrl ? (
            <>
              <label>{tr(t, "audioPreview", "Audio Preview")}</label>
              <audio controls src={audioUrl} />
            </>
          ) : null}

          <button disabled={isTranscribing} onClick={transcribe} type="button">
            {isTranscribing ? tr(t, "transcribing", "Transcribing...") : tr(t, "transcribe", "Transcribe")}
          </button>

          <label>{tr(t, "translationTargetLanguage", "Target Language")}</label>
          <select value={targetLanguage} onChange={(event) => setTargetLanguage(event.target.value)}>
            {LANGUAGE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {tr(t, option.key, option.fallback)}
              </option>
            ))}
          </select>

          <button disabled={isTranslating || !transcript.trim()} onClick={translate} type="button">
            {isTranslating ? tr(t, "translating", "Translating...") : tr(t, "processTranslation", "Translate")}
          </button>
        </div>

        <p style={{ marginTop: "0.75rem" }}>
          <small>{tr(t, "demoHint", "Tip: keep Mock mode ON for a stable stage demo.")}</small>
        </p>
      </article>

      <article className="panel">
        {error ? <p className="error-text">{error}</p> : null}

        <h3>{tr(t, "transcript", "Transcript")}</h3>
        <p><strong>{tr(t, "detectedLanguage", "Detected Language")}:</strong> {detectedLanguage}</p>
        <pre style={{ whiteSpace: "pre-wrap", background: "#f8fafc", borderRadius: 10, padding: "0.75rem" }}>
          {transcript || tr(t, "noTranscriptYet", "No transcript yet.")}
        </pre>

        <h3>{tr(t, "translatedText", "Translated Text")}</h3>
        <pre style={{ whiteSpace: "pre-wrap", background: "#f8fafc", borderRadius: 10, padding: "0.75rem" }}>
          {translatedText || tr(t, "noTranslationYet", "No translation yet.")}
        </pre>
      </article>
    </section>
  );
}
