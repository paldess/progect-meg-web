function loadPhones() {
  var xhr = new XMLHttpRequest();
  var json = JSON.stringify({name: 'Hello, wold!'});
   
  xhr.onreadystatechange = function () {
  if (xhr.readyState === 4 && xhr.status === 200) {
      document.getElementById('result').innerHTML = JSON.parse(xhr.responseText);
      }; 
  };
  xhr.open('GET', 'http://83.220.173.56:5000/hello', false);
  xhr.send();
}

function predicts() {
  var xhr = new XMLHttpRequest();
  var x = document.getElementById('textar').value;
  var json = JSON.stringify({text: x});
  
  xhr.onreadystatechange = function() {
  if (xhr.readyState === 4 && xhr.status === 200) {
      var out = JSON.parse(xhr.responseText);
      console.log(out)
      document.getElementById('result_predict').innerHTML = out[0];
      document.getElementById('result_predict_proba').innerHTML = out[1];
      if (out[0] === 1) {
        document.getElementById('result_predict_img').innerHTML = '<img id="image" src="img/fake.png" style="width: 95%; height: 95%; margin-top: 0;">';
      } else if (out[0] === 0) {
        document.getElementById('result_predict_img').innerHTML = '<img id="image" src="img/not_fake.png" style="width: 95%; height: 95%; margin-top: 0;">';
      };
    };
  };
  xhr.open('POST', 'http://83.220.173.56:5000/predict', false);
  xhr.send([json]);
 }

function clears() {
  document.getElementById('textar').value = '';
  document.getElementById('result_predict').innerHTML = '';
  document.getElementById('result_predict_proba').innerHTML = '';
  document.getElementById('result_predict_img').innerHTML = '';
}

function clears_2() {
  document.getElementById('result_predict').innerHTML = '';
  document.getElementById('result_predict_proba').innerHTML = '';
  document.getElementById('result_list').innerHTML = '';
}

function predicts_megafon() {
    document.getElementById('result_predict_proba').innerHTML = '';
    document.getElementById('result_predict').innerHTML = 'Ожидание расчетов. Подождите...';
    document.getElementById('result_list').innerHTML = '';
    setTimeout(predicts_mega, 500);
}



function predicts_mega() {
  var xhr = new XMLHttpRequest();
  var id_ab = document.getElementById('ID').value;
  var time_month = document.getElementById('time').value;
  var service_ab = document.getElementById('service').value;
  console.log(time_month)
  var json = JSON.stringify({id: id_ab, time: time_month, service: service_ab});
  
  xhr.onreadystatechange = function() {
  if (xhr.readyState === 4 && xhr.status === 200) {
      var out = JSON.parse(xhr.responseText);
      console.log(out)
      
      document.getElementById('result_predict_proba').innerHTML = out[0];
      document.getElementById('result_predict').innerHTML = out[1];
      document.getElementById('result_list').innerHTML = out[2];
    };
  };
  xhr.open('POST', 'http://83.220.173.56:5000/predict_megafon', false);
  xhr.send([json]);
 }

