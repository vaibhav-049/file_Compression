document.addEventListener("DOMContentLoaded", function () {
  // DOM Elements
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const fileInfo = document.getElementById("fileInfo");
  const fileName = document.getElementById("fileName");
  const fileSize = document.getElementById("fileSize");
  const fileType = document.getElementById("fileType");
  const compressionOptions = document.getElementById("compressionOptions");
  const imageOptions = document.getElementById("imageOptions");
  const quality = document.getElementById("quality");
  const qualityValue = document.getElementById("qualityValue");
  const compressBtn = document.getElementById("compressBtn");
  const result = document.getElementById("result");
  const compressedSize = document.getElementById("compressedSize");
  const compressionRatio = document.getElementById("compressionRatio");
  const downloadBtn = document.getElementById("downloadBtn");
  const typeButtons = document.querySelectorAll(".type-btn");
  const modeButtons = document.querySelectorAll(".mode-btn");
  const resetBtn = document.getElementById("resetBtn");
  const filesList = document.getElementById("filesList");
  const filesGrid = document.getElementById("filesGrid");
  const removeAllBtn = document.getElementById("removeAllBtn");
  const processAllBtn = document.getElementById("processAllBtn");
  const browseBtn = document.querySelector(".browse-btn");
  let currentFile = null;
  let currentType = "text";
  let currentMode = "compress";
  let filesQueue = new Map();
  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }
  function getFileIcon(filename) {
    const ext = filename.split(".").pop().toLowerCase();
    switch (ext) {
      case "txt":
      case "csv":
      case "log":
      case "xml":
        return "fa-file-text";
      case "jpg":
      case "jpeg":
      case "png":
      case "gif":
      case "bmp":
        return "fa-file-image";
      case "pdf":
        return "fa-file-pdf";
      case "huff":
        return "fa-file-archive";
      default:
        return "fa-file";
    }
  }
  async function processFile(file) {
    return new Promise(async (resolve, reject) => {
      try {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("type", currentType);
        if (currentType === "image") {
          formData.append("quality", quality.value);
        }
        const response = await fetch("/" + currentMode, {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        if (!response.ok) {
          throw new Error(
            data.error || `HTTP error! status: ${response.status}`
          );
        }
        if (data.error) {
          throw new Error(data.error);
        }
        resolve({
          url: data.download_url,
          size: data.compressed_size,
          ratio: data.compression_ratio,
        });
      } catch (error) {
        reject(error);
      }
    });
  }
  function updateFileStatus(file, status, message = "") {
    for (const [fileId, fileData] of filesQueue.entries()) {
      if (fileData.file === file) {
        const fileItem = document.getElementById(`file-${fileId}`);
        if (fileItem) {
          const statusSpan = fileItem.querySelector(".file-item-status");
          statusSpan.className = `file-item-status status-${status}`;
          statusSpan.textContent =
            status.charAt(0).toUpperCase() + status.slice(1);
          if (message) {
            statusSpan.title = message;
          }
        }
        break;
      }
    }
  }
  function validateFile(file) {
    if (!file) return false;
    const ext = "." + file.name.split(".").pop().toLowerCase();
    const validExtensions = {
      compress: {
        text: [".txt", ".csv", ".log", ".html", ".xml"],
        image: [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        pdf: [".pdf"],
      },
      decompress: {
        text: [".huff"],
        image: [".png", ".jpg", ".jpeg"],
        pdf: [".pdf"],
      },
    };
    if (currentMode === "compress") {
      for (const [type, extensions] of Object.entries(
        validExtensions.compress
      )) {
        if (extensions.includes(ext)) {
          if (currentType !== type) {
            currentType = type;
            typeButtons.forEach((btn) => {
              btn.classList.toggle("active", btn.dataset.type === type);
            });
            imageOptions.style.display = type === "image" ? "block" : "none";
          }
          return true;
        }
      }
    }
    else if (currentMode === "decompress") {
      if (ext === ".huff") {
        currentType = "text";
        typeButtons.forEach((btn) => {
          btn.classList.toggle("active", btn.dataset.type === "text");
        });
        return true;
      }
    }
    return false;
  }
  function addFileToQueue(file) {
    const fileId = Date.now() + "-" + file.name;
    filesQueue.set(fileId, {
      file: file,
      status: "pending",
      result: null,
    });
    const fileItem = document.createElement("div");
    fileItem.className = "file-item";
    fileItem.id = `file-${fileId}`;
    fileItem.innerHTML = `
      <div class="file-item-info">
        <i class="fas ${getFileIcon(file.name)}"></i>
        <span class="file-item-name">${file.name}</span>
        <span class="file-item-size">${formatFileSize(file.size)}</span>
        <span class="file-item-status status-pending">Pending</span>
      </div>
      <div class="file-item-actions">
        <button class="remove-file-btn" data-file-id="${fileId}">
          <i class="fas fa-times"></i>
        </button>
      </div>
    `;
    filesGrid.appendChild(fileItem);
    filesList.style.display = "block";
    fileItem.querySelector(".remove-file-btn").addEventListener("click", () => {
      filesQueue.delete(fileId);
      fileItem.remove();
      if (filesQueue.size === 0) {
        filesList.style.display = "none";
      }
    });
    validateFile(file);
  }
  function handleFiles(files) {
    if (!files || files.length === 0) return;

    Array.from(files).forEach((file) => {
      const existingFile = Array.from(filesQueue.values()).find(
        (f) => f.file.name === file.name && f.file.size === file.size
      );

      if (!existingFile) {
        addFileToQueue(file);
      }
    });
  }
  browseBtn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    fileInput.click();
  });
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });
  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files);
    }
  });
  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files);
    }
  });
  typeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      typeButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
      currentType = button.dataset.type;
      imageOptions.style.display = currentType === "image" ? "block" : "none";
    });
  });
  modeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      modeButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
      currentMode = button.dataset.mode;
      if (currentMode === "decompress") {
        document.querySelector(".compression-types").style.display = "none";
        currentType = "text";
        typeButtons.forEach((btn) => {
          btn.classList.toggle("active", btn.dataset.type === "text");
        });
      } else {
        document.querySelector(".compression-types").style.display = "flex";
      }
      imageOptions.style.display = "none";
    });
  });
  quality.addEventListener("input", () => {
    qualityValue.textContent = quality.value;
  });
  removeAllBtn.addEventListener("click", () => {
    filesQueue.clear();
    filesGrid.innerHTML = "";
    filesList.style.display = "none";
    fileInfo.style.display = "none";
    compressionOptions.style.display = "none";
    result.style.display = "none";
  });
  processAllBtn.addEventListener("click", async () => {
    if (filesQueue.size === 0) {
      alert("No files selected. Please add files first.");
      return;
    }
    let hasValidFiles = false;
    const processPromises = [];
    for (const [fileId, fileData] of filesQueue) {
      const file = fileData.file;
      const fileItem = document.getElementById(`file-${fileId}`);
      const statusSpan = fileItem.querySelector(".file-item-status");
      try {
        if (validateFile(file)) {
          hasValidFiles = true;
          statusSpan.className = "file-item-status status-pending";
          statusSpan.textContent = "Pending";
          const processPromise = (async () => {
            try {
              statusSpan.className = "file-item-status status-processing";
              statusSpan.textContent = "Processing";
              const result = await processFile(file);
              const actionsDiv = fileItem.querySelector(".file-item-actions");
              statusSpan.className = "file-item-status status-completed";
              statusSpan.textContent = "Completed";
              if (!actionsDiv.querySelector(".download-file-btn")) {
                const downloadBtn = document.createElement("a");
                downloadBtn.href = result.url;
                downloadBtn.className = "download-file-btn";
                downloadBtn.title = "Download processed file";
                downloadBtn.innerHTML = '<i class="fas fa-download"></i>';
                actionsDiv.insertBefore(downloadBtn, actionsDiv.firstChild);
              }
              if (!fileItem.querySelector(".file-item-compression-info")) {
                const sizeInfo = document.createElement("span");
                sizeInfo.className = "file-item-compression-info";
                sizeInfo.textContent = `${formatFileSize(
                  result.size
                )} (${result.ratio.toFixed(2)} % smaller)`;
                fileItem.querySelector(".file-item-info").appendChild(sizeInfo);
              }
            } catch (error) {
              console.error(`Error processing ${file.name}:`, error);
              statusSpan.className = "file-item-status status-error";
              statusSpan.textContent = "Error";
              statusSpan.title = error.message;
            }
          })();
          processPromises.push(processPromise);
        } else {
          statusSpan.className = "file-item-status status-error";
          statusSpan.textContent = "Invalid Type";
          statusSpan.title = `File type not supported for ${currentMode} mode`;
        }
      } catch (error) {
        console.error(`Error validating ${file.name}:`, error);
        statusSpan.className = "file-item-status status-error";
        statusSpan.textContent = "Error";
        statusSpan.title = error.message;
      }
    }
    if (!hasValidFiles) {
      alert(
        "No valid files to process. Please check the file types and try again."
      );
      return;
    }
    try {
      await Promise.all(processPromises);
    } catch (error) {
      console.error("Error processing files:", error);
    }
  });
  resetBtn.addEventListener("click", () => {
    fileInput.value = "";
    filesQueue.clear();
    filesGrid.innerHTML = "";
    filesList.style.display = "none";
    fileInfo.style.display = "none";
    compressionOptions.style.display = "none";
    result.style.display = "none";
    imageOptions.style.display = "none";
    currentMode = "compress";
    currentType = "text";
    modeButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.mode === "compress");
    });
    typeButtons.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.type === "text");
    });
    document.querySelector(".compression-types").style.display = "flex";
  });
});
