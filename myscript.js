window.onload = function() {
  setInterval(function() {
    // scroll to bottom of div
    var obj = document.getElementById('log');
    obj.scrollTop = obj.scrollHeight;
  }, 1000);
};