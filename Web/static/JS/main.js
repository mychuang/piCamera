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