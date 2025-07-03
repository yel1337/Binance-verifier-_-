function sensorsdata2015jssdkcross(screen_height, screen_width, userAgent) {
  function randomId() {
    // 生成类似浏览器的ID
    return (
      Math.random().toString(36).substr(2, 15) +
      '-' +
      Math.random().toString(36).substr(2, 15) +
      '-' +
      Math.random().toString(36).substr(2, 8) +
      '-' +
      Math.random().toString(36).substr(2, 7) +
      '-' +
      Math.random().toString(36).substr(2, 15)
    ).substr(0, 48);
  }

  const id = randomId();
  const obj = {
    distinct_id: id,
    first_id: "",
    props: {
      $latest_traffic_source_type: "直接流量",
      $latest_search_keyword: "未取到值_直接打开",
      $latest_referrer: ""
    },
    identities: btoa(
      JSON.stringify({
        $identity_cookie_id: id
      })
    ),
    history_login_id: {
      name: "",
      value: ""
    }
  };
  // URL编码
  const encoded = encodeURIComponent(JSON.stringify(obj));
  return `sensorsdata2015jssdkcross=${encoded}`;
}