<script>
function bestCropThisSeason() {
  const month = new Date().getMonth() + 1; // 1–12

  let season = "";
  let crops = [];

  // 🌧 KHARIF: June – October
  if (month >= 6 && month <= 10) {
    season = "Kharif Season";
    crops = ["Rice", "Maize", "Cotton", "Soybean"];
  }

  // ❄️ RABI: October – March
  else if (month >= 10 || month <= 3) {
    season = "Rabi Season";
    crops = ["Wheat", "Mustard", "Gram", "Barley"];
  }

  // ☀️ ZAID: March – June
  else {
    season = "Zaid Season";
    crops = ["Watermelon", "Muskmelon", "Cucumber", "Bitter Gourd"];
  }

  // Show result
  document.getElementById("seasonResult").style.display = "block";
  document.getElementById("seasonTitle").innerText =
    `Best Crops for ${season}`;

  const list = document.getElementById("cropList");
  list.innerHTML = "";

  crops.forEach(crop => {
    const li = document.createElement("li");
    li.innerText = crop;
    list.appendChild(li);
  });
}
let isSpeaking = false;

function speakText(text){

  if(isSpeaking){
    speechSynthesis.cancel();
    isSpeaking = false;
    return;
  }

  const speech = new SpeechSynthesisUtterance(text);
  speech.lang = "en-US";

  speechSynthesis.speak(speech);
  isSpeaking = true;

  speech.onend = function(){
    isSpeaking = false;
  };

}

</script>
