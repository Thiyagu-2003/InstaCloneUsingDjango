document.addEventListener('DOMContentLoaded', function() {
    const notificationSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/notifications/'
    );

    const unreadBadge = document.getElementById('unread-messages-badge');

    notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'unread_count') {
            updateUnreadBadge(data.count);
        }
    };

    function updateUnreadBadge(count) {
        if (count > 0) {
            unreadBadge.textContent = count;
            unreadBadge.style.display = 'inline';
        } else {
            unreadBadge.style.display = 'none';
        }
    }

    notificationSocket.onclose = function(e) {
        console.log('Notification socket closed unexpectedly');
        setTimeout(function() {
            console.log('Attempting to reconnect...');
            window.location.reload();
        }, 3000);
    };
});