
const uploadBtn = document.getElementById("uploadBtn");
const askBtn = document.getElementById("askBtn");

uploadBtn.addEventListener("click", uploadFile);
askBtn.addEventListener("click", askQuestion);


async function uploadFile() {
    clearError();
    const fileInput = document.getElementById("fileInput");
    const uploadStatus = document.getElementById("uploadStatus");
    const chatSection = document.getElementById("chatSection");

    if (!fileInput.files.length) {
        showError("Please select a PDF or TXT file.");
        return;
    }

    const file = fileInput.files[0];

    if (!(file.name.endsWith(".pdf")|| file.name.endsWith(".txt"))) {
        showError("Only PDF and TXT files are allowed.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showLoading(true);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Upload failed.");
        }

        uploadStatus.innerText = "Document processed successfully!";
        chatSection.style.display = "block";

    } catch (error) {
        showError(error.messagee);
    }

    showLoading(false);
}

async function askQuestion() {
    clearError();
    const questionInput = document.getElementById("questionInput");
    const chatBox = document.getElementById("chatBox");

    const question = questionInput.value.trim();

    if (!question) {
        showError("Please enter a question.");
        return;
    }

    showLoading(true);

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error getting answer.");
        }

        const data = await response.json();

        addMessage("You", question);
        addMessage("Assistant", data.response);

        questionInput.value = "";

    } catch (error) {
        showError(error.message );
    }

    showLoading(false);
}

function addMessage(sender, text) {
    const chatBox = document.getElementById("chatBox");

    const messageDiv = document.createElement("div");
    messageDiv.className = "message";
    sen= document.createTextNode(sender);
    messageDiv.innerHTML =formatResponse(text);
    chatBox.appendChild(sen);
    chatBox.appendChild(messageDiv);
}

function showError(message) {
    const errorBox = document.getElementById("errorBox");
    errorBox.innerText = message;
    errorBox.style.display = "block";
}

function clearError() {
    document.getElementById("errorBox").style.display = "none";
}

function showLoading(state) {
    document.getElementById("loading").style.display = state ? "block" : "none";
}
function formatResponse(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    text = text.replace(/\* /g, "• ");
    text = text.replace(/\n/g, "<br>");
    return text;
}
