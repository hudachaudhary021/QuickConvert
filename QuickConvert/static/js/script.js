(function () {
  "use strict";

  /* ------------------------------------------------------------------ */
  /* Mobile navigation toggle                                           */
  /* ------------------------------------------------------------------ */

  const navToggle = document.getElementById("navToggle");
  const navMenu = document.getElementById("navMenu");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      const isOpen = navMenu.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    navMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navMenu.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* FAQ accordion                                                       */
  /* ------------------------------------------------------------------ */

  const accordionItems = document.querySelectorAll(".accordion__item");
  accordionItems.forEach(function (item) {
    const trigger = item.querySelector(".accordion__trigger");
    if (!trigger) return;

    trigger.addEventListener("click", function () {
      const isOpen = item.classList.contains("is-open");

      accordionItems.forEach(function (other) {
        other.classList.remove("is-open");
        const otherTrigger = other.querySelector(".accordion__trigger");
        if (otherTrigger) otherTrigger.setAttribute("aria-expanded", "false");
      });

      if (!isOpen) {
        item.classList.add("is-open");
        trigger.setAttribute("aria-expanded", "true");
      }
    });
  });

  /* ------------------------------------------------------------------ */
  /* Converter widget (only present on the home page)                    */
  /* ------------------------------------------------------------------ */

  const dropzone = document.getElementById("dropzone");
  if (!dropzone) return; // Not on the home page, nothing else to do.

  const fileInput = document.getElementById("fileInput");
  const dropzoneTitle = document.getElementById("dropzoneTitle");
  const fileNameDisplay = document.getElementById("fileNameDisplay");
  const convertForm = document.getElementById("convertForm");
  const convertBtn = document.getElementById("convertBtn");
  const formError = document.getElementById("formError");
  const progressBar = document.getElementById("progressBar");
  const progressFill = document.getElementById("progressFill");
  const resultCard = document.getElementById("resultCard");
  const downloadLink = document.getElementById("downloadLink");
  const convertAnotherBtn = document.getElementById("convertAnotherBtn");
  const tabWordToPdf = document.getElementById("tabWordToPdf");
  const tabPdfToWord = document.getElementById("tabPdfToWord");

  const MAX_SIZE_BYTES = 20 * 1024 * 1024;

  const MODES = {
    "word-to-pdf": {
      extensions: [".docx", ".doc"],
      accept: ".docx,.doc",
      endpoint: window.QUICKCONVERT_ENDPOINTS
        ? window.QUICKCONVERT_ENDPOINTS.wordToPdf
        : "/convert/word-to-pdf",
      dropLabel: "Drag & drop your .docx file here",
    },
    "pdf-to-word": {
      extensions: [".pdf"],
      accept: ".pdf",
      endpoint: window.QUICKCONVERT_ENDPOINTS
        ? window.QUICKCONVERT_ENDPOINTS.pdfToWord
        : "/convert/pdf-to-word",
      dropLabel: "Drag & drop your .pdf file here",
    },
  };

  let currentMode = "word-to-pdf";
  let selectedFile = null;

  function setMode(mode) {
    currentMode = mode;
    selectedFile = null;
    fileInput.value = "";
    fileNameDisplay.textContent = "";
    convertBtn.disabled = true;
    formError.textContent = "";
    dropzoneTitle.textContent = MODES[mode].dropLabel;
    fileInput.setAttribute("accept", MODES[mode].accept);

    tabWordToPdf.classList.toggle("is-active", mode === "word-to-pdf");
    tabPdfToWord.classList.toggle("is-active", mode === "pdf-to-word");

    resultCard.hidden = true;
    convertForm.hidden = false;
  }

  tabWordToPdf.addEventListener("click", function () {
    setMode("word-to-pdf");
  });
  tabPdfToWord.addEventListener("click", function () {
    setMode("pdf-to-word");
  });

  function extensionOf(filename) {
    const idx = filename.lastIndexOf(".");
    return idx === -1 ? "" : filename.slice(idx).toLowerCase();
  }

  function validateFile(file) {
    if (!file) return "Please choose a file.";

    const ext = extensionOf(file.name);
    if (!MODES[currentMode].extensions.includes(ext)) {
      return "Invalid file type. Allowed: " + MODES[currentMode].extensions.join(", ");
    }

    if (file.size > MAX_SIZE_BYTES) {
      return "File is too large. Maximum size is 20MB.";
    }

    if (file.size === 0) {
      return "This file appears to be empty.";
    }

    return null;
  }

  function handleFileSelection(file) {
    const error = validateFile(file);
    formError.textContent = error || "";

    if (error) {
      selectedFile = null;
      fileNameDisplay.textContent = "";
      convertBtn.disabled = true;
      return;
    }

    selectedFile = file;
    fileNameDisplay.textContent = file.name;
    convertBtn.disabled = false;
  }

  dropzone.addEventListener("click", function () {
    fileInput.click();
  });

  dropzone.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInput.click();
    }
  });

  fileInput.addEventListener("change", function () {
    if (fileInput.files && fileInput.files[0]) {
      handleFileSelection(fileInput.files[0]);
    }
  });

  ["dragenter", "dragover"].forEach(function (eventName) {
    dropzone.addEventListener(eventName, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("is-dragover");
    });
  });

  ["dragleave", "drop"].forEach(function (eventName) {
    dropzone.addEventListener(eventName, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("is-dragover");
    });
  });

  dropzone.addEventListener("drop", function (e) {
    const dt = e.dataTransfer;
    if (dt && dt.files && dt.files[0]) {
      handleFileSelection(dt.files[0]);
    }
  });

  function uploadWithProgress(url, file) {
    return new Promise(function (resolve, reject) {
      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      formData.append("file", file);

      xhr.open("POST", url, true);

      xhr.upload.addEventListener("progress", function (event) {
        if (event.lengthComputable) {
          const percent = Math.round((event.loaded / event.total) * 100);
          progressFill.style.width = percent + "%";
        }
      });

      xhr.onload = function () {
        let data;
        try {
          data = JSON.parse(xhr.responseText);
        } catch (err) {
          reject(new Error("Unexpected response from server."));
          return;
        }

        if (xhr.status >= 200 && xhr.status < 300 && data.success) {
          resolve(data);
        } else {
          reject(new Error(data.error || "Conversion failed. Please try again."));
        }
      };

      xhr.onerror = function () {
        reject(new Error("Network error. Please check your connection and try again."));
      };

      xhr.send(formData);
    });
  }

  convertForm.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!selectedFile) {
      formError.textContent = "Please choose a file first.";
      return;
    }

    const validationError = validateFile(selectedFile);
    if (validationError) {
      formError.textContent = validationError;
      return;
    }

    formError.textContent = "";
    convertBtn.disabled = true;
    convertBtn.textContent = "Converting…";
    progressBar.hidden = false;
    progressFill.style.width = "0%";

    uploadWithProgress(MODES[currentMode].endpoint, selectedFile)
      .then(function (data) {
        progressFill.style.width = "100%";
        downloadLink.href = data.download_url;
        downloadLink.setAttribute("download", data.filename || "");
        convertForm.hidden = true;
        resultCard.hidden = false;
      })
      .catch(function (err) {
        formError.textContent = err.message || "Something went wrong. Please try again.";
      })
      .finally(function () {
        convertBtn.disabled = false;
        convertBtn.textContent = "Convert now";
        progressBar.hidden = true;
      });
  });

  convertAnotherBtn.addEventListener("click", function () {
    setMode(currentMode);
  });

  // Initialize default mode state.
  setMode(currentMode);
})();
