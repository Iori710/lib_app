document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var ISBN = calendarEl.getAttribute('data-isbn'); // ISBNを取得
    axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        // 日付をクリック、または範囲を選択したイベント
        selectable: true,
        select: function (info) {
            let checkReserve = confirm("予約を追加しますか？\n" +
                "開始日: " + info.start + "\n" +
                "終了日: " + info.end);
            if (checkReserve) {
                
        // 登録処理の呼び出し
                axios
                    .post(`/reserving/${ISBN}`, {
                        lending_start: info.start.valueOf(),
                        lending_end: info.end.valueOf(),
                    })
                    .then(() => {
                        window.location.href = `/reserving/${ISBN}`;
                    })
                    .catch(() => {
        // バリデーションエラーなど
                        alert("予約ができませんでした。");
                    }); 
            }
        },
    });
    calendar.render();
  });