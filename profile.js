const phone = document.getElementById("phone");
const aadhaar = document.getElementById("aadhaar");
const kisan = document.getElementById("kisan");

const phoneError = document.getElementById("phoneError");
const aadhaarError = document.getElementById("aadhaarError");
const kisanError = document.getElementById("kisanError");

/* Indian Phone */
phone.addEventListener("input", () => {
  phoneError.textContent =
    /^[6-9]\d{9}$/.test(phone.value) ? "" : "Invalid Indian phone number";
});

/* Aadhaar */
aadhaar.addEventListener("input", () => {
  aadhaarError.textContent =
    /^\d{12}$/.test(aadhaar.value) ? "" : "Aadhaar must be 12 digits";
});

/* Kisan Card */
kisan.addEventListener("input", () => {
  kisanError.textContent =
    /^\d{16}$/.test(kisan.value) ? "" : "Kisan card must be 16 digits";
});

/* Save */
document.getElementById("profileForm").addEventListener("submit", e => {
  e.preventDefault();

  if (phoneError.textContent || aadhaarError.textContent || kisanError.textContent) {
    alert("Fix errors first");
    return;
  }

  const data = new FormData();
  data.append("phone", phone.value);
  data.append("aadhaar", aadhaar.value);
  data.append("kisan", kisan.value);
  data.append("profilePic", profilePic.files[0]);
  data.append("aadhaarPic", aadhaarPic.files[0]);
  data.append("kisanPic", kisanPic.files[0]);

  fetch("/save_profile", { method: "POST", body: data })
    .then(r => r.json())
    .then(d => document.getElementById("successMsg").innerText = d.message);
});
document.getElementById("profileForm").addEventListener("submit", e => {
  e.preventDefault();

  const data = new FormData(e.target);

  fetch("/api/save-profile", {
    method: "POST",
    body: data
  })
  .then(res => res.json())
  .then(d => alert("Profile saved successfully"));
});

