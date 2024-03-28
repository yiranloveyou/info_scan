/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
particlesJS.load('particlesjs-config.json', '{{url_for("/particlesjs-config.json")}}', function() {
    console.log('callback - particlesjs-config.json config loaded');
  });
  