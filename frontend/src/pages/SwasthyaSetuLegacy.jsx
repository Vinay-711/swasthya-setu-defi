import React, { useEffect } from 'react';

import '../styles/app.css'; // Make sure styles are globally loaded or import a specific CSS

export default function SwasthyaSetuLegacy() {
  useEffect(() => {
    // Append scripts dynamically or just let them run if imported
    const script = document.createElement('script');
    script.src = '/swasthyasetu.js'; // We will extract JS to public/swasthyasetu.js
    script.async = true;
    document.body.appendChild(script);
    return () => document.body.removeChild(script);
  }, []);

  return (
    <div dangerouslySetInnerHTML={{__html: `
