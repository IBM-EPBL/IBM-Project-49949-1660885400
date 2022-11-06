const fileDropArea = document.querySelector(`[data-item="file-drop-area"]`);
const classifyBtn = document.querySelector(`[data-item="classify-btn"]`);

const highlight = (event) => {
  event.preventDefault();
  event.stopPropagation();
  fileDropArea.classList.add("file-enter");
};

const unhighlight = (event) => {
  event.preventDefault();
  event.stopPropagation();
  fileDropArea.classList.remove("file-enter");
};

fileDropArea.addEventListener("dragenter", highlight, false);
fileDropArea.addEventListener("dragover", highlight, false);

fileDropArea.addEventListener("dragleave", unhighlight, false);
fileDropArea.addEventListener(
  "drop",
  (event) => {
    unhighlight(event);
    const file = event.dataTransfer.files[0];
  },
  false
);
