document.addEventListener('DOMContentLoaded', function() {
    let notificationSocket;
    const unreadBadge = document.getElementById('unread-messages-badge');

    function connectNotificationSocket() {
        notificationSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/notifications/'
        );

        notificationSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.type === 'unread_count') {
                updateUnreadBadge(data.count);
            }
            // Optionally handle other notification types here
        };

        notificationSocket.onclose = function(e) {
            console.log('Notification socket closed unexpectedly');
            setTimeout(function() {
                console.log('Attempting to reconnect...');
                connectNotificationSocket(); // Reconnect without refreshing the page
            }, 3000);
        };
    }

    function updateUnreadBadge(count) {
        if (count > 0) {
            unreadBadge.textContent = count;
            unreadBadge.style.display = 'inline';
        } else {
            unreadBadge.style.display = 'none';
        }
    }

    connectNotificationSocket();
});