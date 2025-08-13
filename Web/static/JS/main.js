function containsDangerousChars(str) {
    const pattern = /['"\\;]|--/g;
    return pattern.test(str);
}

function handleLogin() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorMsg = document.getElementById("errorMsg");

    if (!username || !password) {
        errorMsg.textContent = "帳號與密碼不可為空";
        return;
    }

    if (containsDangerousChars(username) || containsDangerousChars(password)) {
        errorMsg.textContent = "輸入中含有非法字元";
        return;
    }

    // 未來可改為發送 POST 請求驗證帳密
    console.log("✅ 驗證成功，前往主畫面");
    setTimeout(() => {
        window.location.href = "/main";
    }, 1000);
}

let currentMode = 1; // 預設模式 1

function updateButtonStates() {
    document.querySelectorAll('.mode-buttons button').forEach(btn => {
        btn.disabled = false;
        btn.style.background = '#4db6ac';
        btn.style.cursor = 'pointer';
    });

    const activeBtn = document.getElementById(`mode-${currentMode}`);
    if (activeBtn) {
        activeBtn.disabled = true;
        activeBtn.style.background = 'gray';
        activeBtn.style.cursor = 'not-allowed';
    }
}

function switchMode(mode) {
    if (mode === currentMode) return; // 避免重複切換
    currentMode = mode;

    const img = document.querySelector('.stream');
    img.src = `/video_feed?mode=${mode}&_=${Date.now()}`;

    updateButtonStates();
}

window.onload = updateButtonStates;