/**
 * For usage, visit Chart.js docs 
 */
usercount=document.getElementById("usercount").innerText;
messagecount=document.getElementById("messagecount").innerText;
postcount=document.getElementById("postcount").innerText;
console.log(usercount, messagecount, postcount);
const pieConfig = {
  type: 'doughnut',
  data: {
    datasets: [
      {
        data: [ usercount,messagecount , postcount],
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: ['#0694a2', '#1c64f2', '#7e3af2'],
        label: 'Dataset 1',
      },
    ],
    labels: ['Users', 'Posts', 'Messages'],
  },
  options: {
    responsive: true,
    cutoutPercentage: 80,
    /**
     * Default legends are ugly and impossible to style.
     * See examples in charts.html to add your own legends
     *  */
    legend: {
      display: false,
    },
  },
}

// change this to the id of your chart element in HMTL
const pieCtx = document.getElementById('pie')
window.myPie = new Chart(pieCtx, pieConfig)
