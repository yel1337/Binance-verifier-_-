# Proxy Rotation System Configuration

## Overview
The new proxy rotation system has been implemented with the following features:

### Key Features:
1. **Smart IP Rotation**: Automatically rotates proxies every 15 minutes to get fresh IPs
2. **Multiple Rotation Methods**: 
   - Smart rotation (prefers fresh IPs)
   - Round-robin rotation
   - Random rotation
3. **Proxy Health Monitoring**: Tracks failed proxies and avoids them
4. **Usage Statistics**: Monitors proxy usage and performance

### Proxy Configuration:
- **Total Proxies**: 30 proxy-jet.io residential proxies
- **IP Refresh Interval**: 15 minutes (as specified)
- **Format**: `username:password@host:port`
- **Provider**: proxy-jet.io

### How It Works:

#### 1. Smart Rotation (Default)
- Prioritizes proxies that haven't been used in 15+ minutes
- Falls back to least recently used if no fresh proxies available
- Automatically tracks usage timestamps

#### 2. Error Handling
- Marks failed proxies as temporarily unavailable
- Automatically retries with different proxies on failure
- Logs proxy failures for monitoring

#### 3. Thread Safety
- Uses threading locks for concurrent access
- Safe for multi-threaded verification processes

### Usage in Code:

```python
from proxy_rotator import proxy_rotator

# Get a smart proxy (recommended)
proxy_dict = proxy_rotator.get_smart_proxy()

# Get round-robin proxy
proxy_dict = proxy_rotator.get_round_robin_proxy()

# Get random proxy
proxy_dict = proxy_rotator.get_random_proxy()

# Use with requests
response = requests.get(url, proxies=proxy_dict)

# Check statistics
proxy_rotator.print_stats()
```

### Integration Points:

1. **Main verification function** (`verify()`): Now uses `proxy_rotator.get_smart_proxy()`
2. **Network testing**: Uses smart rotation for initial connectivity test
3. **Error handling**: Marks failed proxies and retries with fresh ones
4. **Statistics**: Displays proxy usage stats periodically

### Benefits:

1. **Fresh IPs**: Each request is more likely to use a different IP
2. **Reduced Rate Limiting**: 15-minute rotation helps avoid detection
3. **Better Success Rate**: Failed proxies are automatically avoided
4. **Load Balancing**: Evenly distributes load across all proxies
5. **Monitoring**: Real-time visibility into proxy performance

### Configuration Options:

You can adjust the rotation behavior by modifying `proxy_rotator.py`:

- `rotation_interval`: Change from 15 minutes to other intervals
- Rotation strategy: Modify the selection logic in `get_fresh_proxy()`
- Error handling: Customize proxy failure detection

### Testing:

Run `test_proxy_rotation.py` to verify the system is working correctly:

```bash
python test_proxy_rotation.py
```

This will test:
- Proxy connectivity
- IP rotation
- Different rotation methods
- Usage statistics
