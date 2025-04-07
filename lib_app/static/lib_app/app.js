document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var ISBN = calendarEl.getAttribute('data-isbn'); // ISBNを取得
    axios.defaults.headers.common['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        // 日付をクリック、または範囲を選択したイベント
        selectable: true,
        select: function (info) {
            let checkReserve = confirm("予約を追加しますか？");
            if (checkReserve) {
                // 登録処理の呼び出し
                axios
                    .post(`/reserving/${ISBN}/`, {
                        lending_start: info.start.valueOf(),
                        lending_end: info.end.valueOf(),
                    })
                    .then(() => {
                        // 成功時に別のURLに遷移
                        window.location.href = `/reserved/${ISBN}/`;
                    })
                    .catch(() => {
                        // バリデーションエラーなど
                        alert("予約ができませんでした。");
                    });
            }
        },

        events: function (info, successCallback, failureCallback) {

            axios
                .post(`/calendar/${ISBN}/`, {
                    start_date: info.start.valueOf(),
                    end_date: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                    // バリデーションエラーなど
                    alert("読み込みに失敗しました");
                });
        },
    });
    calendar.render();
});