"""
Performance Monitoring Service
Monitors system resources, performance metrics, and provides optimization recommendations
"""

import asyncio
import psutil
import time
import json
import os
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import deque
import logging
import GPUtil
import platform
from concurrent.futures import ThreadPoolExecutor
import gc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    memory_total_gb: float
    disk_usage_percent: float
    disk_free_gb: float
    disk_total_gb: float
    gpu_usage: Optional[float] = None
    gpu_memory_percent: Optional[float] = None
    gpu_memory_used_gb: Optional[float] = None
    gpu_memory_total_gb: Optional[float] = None
    network_sent_mb: float = 0.0
    network_recv_mb: float = 0.0
    active_processes: int = 0
    load_average: Optional[float] = None

@dataclass
class ProcessMetrics:
    """Process-specific metrics"""
    timestamp: datetime
    process_name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    threads: int
    status: str
    duration: float

@dataclass
class PerformanceAlert:
    """Performance alert"""
    timestamp: datetime
    level: str  # 'warning', 'critical'
    category: str  # 'cpu', 'memory', 'disk', 'gpu'
    message: str
    value: float
    threshold: float
    recommendation: str

class PerformanceMonitor:
    def __init__(self, cache_dir: str = "cache/performance", 
                 monitoring_interval: float = 5.0,
                 history_size: int = 1000):
        """Initialize performance monitor"""
        self.cache_dir = cache_dir
        self.monitoring_interval = monitoring_interval
        self.history_size = history_size
        
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Metrics storage
        self.system_metrics_history = deque(maxlen=history_size)
        self.process_metrics_history = deque(maxlen=history_size)
        self.alerts_history = deque(maxlen=100)
        
        # Alert cooldown tracking (category -> last_alert_time)
        self.alert_cooldown = {}
        self.alert_cooldown_period = 300  # 5 minutes between similar alerts
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Performance thresholds (adjusted for better performance)
        self.thresholds = {
            'cpu_warning': 80.0,
            'cpu_critical': 95.0,
            'memory_warning': 90.0,  # Increased from 85% to 90%
            'memory_critical': 97.0,  # Increased from 95% to 97%
            'disk_warning': 90.0,
            'disk_critical': 98.0,
            'gpu_warning': 90.0,
            'gpu_critical': 98.0
        }
        
        # Network baseline
        self.network_baseline = None
        self._update_network_baseline()
        
        # Performance statistics
        self.stats = {
            'monitoring_start_time': None,
            'total_alerts': 0,
            'critical_alerts': 0,
            'average_cpu': 0.0,
            'average_memory': 0.0,
            'peak_cpu': 0.0,
            'peak_memory': 0.0,
            'uptime_hours': 0.0
        }
        
        # Load historical data
        self._load_historical_data()
        
        # Start monitoring
        self.start_monitoring()
    
    def _update_network_baseline(self):
        """Update network baseline for calculating deltas"""
        try:
            net_io = psutil.net_io_counters()
            self.network_baseline = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Failed to update network baseline: {e}")
    
    def _load_historical_data(self):
        """Load historical performance data"""
        try:
            metrics_file = os.path.join(self.cache_dir, "metrics_history.json")
            if os.path.exists(metrics_file):
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load system metrics
                for metric_data in data.get('system_metrics', [])[-self.history_size:]:
                    metric = SystemMetrics(**metric_data)
                    metric.timestamp = datetime.fromisoformat(metric_data['timestamp'])
                    self.system_metrics_history.append(metric)
                
                # Load process metrics
                for metric_data in data.get('process_metrics', [])[-self.history_size:]:
                    metric = ProcessMetrics(**metric_data)
                    metric.timestamp = datetime.fromisoformat(metric_data['timestamp'])
                    self.process_metrics_history.append(metric)
                
                # Load alerts
                for alert_data in data.get('alerts', [])[-100:]:
                    alert = PerformanceAlert(**alert_data)
                    alert.timestamp = datetime.fromisoformat(alert_data['timestamp'])
                    self.alerts_history.append(alert)
                
                # Load stats
                self.stats.update(data.get('stats', {}))
                if self.stats.get('monitoring_start_time'):
                    self.stats['monitoring_start_time'] = datetime.fromisoformat(
                        self.stats['monitoring_start_time']
                    )
                
                logger.info(f"Loaded {len(self.system_metrics_history)} historical metrics")
                
        except Exception as e:
            logger.error(f"Failed to load historical data: {e}")
    
    def _save_historical_data(self):
        """Save historical performance data"""
        try:
            metrics_file = os.path.join(self.cache_dir, "metrics_history.json")
            
            # Prepare data for serialization
            data = {
                'system_metrics': [],
                'process_metrics': [],
                'alerts': [],
                'stats': dict(self.stats)
            }
            
            # Convert system metrics
            for metric in list(self.system_metrics_history)[-500:]:  # Save last 500
                metric_data = asdict(metric)
                metric_data['timestamp'] = metric.timestamp.isoformat()
                data['system_metrics'].append(metric_data)
            
            # Convert process metrics
            for metric in list(self.process_metrics_history)[-500:]:  # Save last 500
                metric_data = asdict(metric)
                metric_data['timestamp'] = metric.timestamp.isoformat()
                data['process_metrics'].append(metric_data)
            
            # Convert alerts
            for alert in list(self.alerts_history):
                alert_data = asdict(alert)
                alert_data['timestamp'] = alert.timestamp.isoformat()
                data['alerts'].append(alert_data)
            
            # Convert stats timestamps
            if self.stats.get('monitoring_start_time'):
                data['stats']['monitoring_start_time'] = self.stats['monitoring_start_time'].isoformat()
            
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save historical data: {e}")
    
    def start_monitoring(self):
        """Start performance monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.stats['monitoring_start_time'] = datetime.now()
            self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10.0)
        self._save_historical_data()
        logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                if system_metrics:
                    self.system_metrics_history.append(system_metrics)
                    self._check_system_alerts(system_metrics)
                    self._update_statistics(system_metrics)
                
                # Collect process metrics for current process
                process_metrics = self._collect_process_metrics()
                if process_metrics:
                    self.process_metrics_history.append(process_metrics)
                
                # Save data periodically
                if len(self.system_metrics_history) % 60 == 0:  # Every 5 minutes
                    self._save_historical_data()
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_system_metrics(self) -> Optional[SystemMetrics]:
        """Collect current system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_usage_percent = (disk.used / disk.total) * 100
            disk_free_gb = disk.free / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # GPU metrics (if available)
            gpu_usage = None
            gpu_memory_percent = None
            gpu_memory_used_gb = None
            gpu_memory_total_gb = None
            
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]  # Use first GPU
                    gpu_usage = gpu.load * 100
                    gpu_memory_percent = gpu.memoryUtil * 100
                    gpu_memory_used_gb = gpu.memoryUsed / 1024
                    gpu_memory_total_gb = gpu.memoryTotal / 1024
            except Exception:
                pass  # GPU monitoring not available
            
            # Network metrics
            network_sent_mb = 0.0
            network_recv_mb = 0.0
            
            try:
                net_io = psutil.net_io_counters()
                if self.network_baseline:
                    time_delta = time.time() - self.network_baseline['timestamp']
                    if time_delta > 0:
                        bytes_sent_delta = net_io.bytes_sent - self.network_baseline['bytes_sent']
                        bytes_recv_delta = net_io.bytes_recv - self.network_baseline['bytes_recv']
                        
                        network_sent_mb = (bytes_sent_delta / time_delta) / (1024**2)
                        network_recv_mb = (bytes_recv_delta / time_delta) / (1024**2)
                
                # Update baseline
                self.network_baseline = {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'timestamp': time.time()
                }
            except Exception:
                pass
            
            # Process count
            active_processes = len(psutil.pids())
            
            # Load average (Unix-like systems)
            load_average = None
            try:
                if hasattr(os, 'getloadavg'):
                    load_average = os.getloadavg()[0]
            except Exception:
                pass
            
            return SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_gb=memory_used_gb,
                memory_total_gb=memory_total_gb,
                disk_usage_percent=disk_usage_percent,
                disk_free_gb=disk_free_gb,
                disk_total_gb=disk_total_gb,
                gpu_usage=gpu_usage,
                gpu_memory_percent=gpu_memory_percent,
                gpu_memory_used_gb=gpu_memory_used_gb,
                gpu_memory_total_gb=gpu_memory_total_gb,
                network_sent_mb=network_sent_mb,
                network_recv_mb=network_recv_mb,
                active_processes=active_processes,
                load_average=load_average
            )
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return None
    
    def _collect_process_metrics(self) -> Optional[ProcessMetrics]:
        """Collect metrics for current process"""
        try:
            process = psutil.Process()
            
            # Get process info
            with process.oneshot():
                cpu_percent = process.cpu_percent()
                memory_info = process.memory_info()
                memory_percent = process.memory_percent()
                memory_mb = memory_info.rss / (1024**2)
                threads = process.num_threads()
                status = process.status()
                create_time = process.create_time()
                duration = time.time() - create_time
            
            return ProcessMetrics(
                timestamp=datetime.now(),
                process_name="veo7-backend",
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_mb=memory_mb,
                threads=threads,
                status=status,
                duration=duration
            )
            
        except Exception as e:
            logger.error(f"Failed to collect process metrics: {e}")
            return None
    
    def _check_system_alerts(self, metrics: SystemMetrics):
        """Check for performance alerts"""
        try:
            alerts = []
            current_time = time.time()
            
            # CPU alerts
            if metrics.cpu_percent >= self.thresholds['cpu_critical']:
                if self._should_send_alert('cpu_critical', current_time):
                    alerts.append(PerformanceAlert(
                        timestamp=datetime.now(),
                        level='critical',
                        category='cpu',
                        message=f'Critical CPU usage: {metrics.cpu_percent:.1f}%',
                        value=metrics.cpu_percent,
                        threshold=self.thresholds['cpu_critical'],
                        recommendation='Consider scaling up CPU resources or optimizing CPU-intensive operations'
                    ))
            elif metrics.cpu_percent >= self.thresholds['cpu_warning']:
                if self._should_send_alert('cpu_warning', current_time):
                    alerts.append(PerformanceAlert(
                        timestamp=datetime.now(),
                        level='warning',
                        category='cpu',
                        message=f'High CPU usage: {metrics.cpu_percent:.1f}%',
                        value=metrics.cpu_percent,
                        threshold=self.thresholds['cpu_warning'],
                        recommendation='Monitor CPU usage and consider optimization if sustained'
                    ))
            
            # Memory alerts with automatic cleanup
            if metrics.memory_percent >= self.thresholds['memory_critical']:
                if self._should_send_alert('memory_critical', current_time):
                    # Trigger automatic cleanup for critical memory usage
                    try:
                        gc.collect()  # Force garbage collection
                        logger.info("Automatic garbage collection triggered due to critical memory usage")
                    except Exception as e:
                        logger.error(f"Failed to trigger automatic cleanup: {e}")
                    
                    alerts.append(PerformanceAlert(
                        timestamp=datetime.now(),
                        level='critical',
                        category='memory',
                        message=f'Critical memory usage: {metrics.memory_percent:.1f}% (auto-cleanup triggered)',
                        value=metrics.memory_percent,
                        threshold=self.thresholds['memory_critical'],
                        recommendation='Immediate action required: restart services or add more RAM'
                    ))
            elif metrics.memory_percent >= self.thresholds['memory_warning']:
                if self._should_send_alert('memory_warning', current_time):
                    alerts.append(PerformanceAlert(
                        timestamp=datetime.now(),
                        level='warning',
                        category='memory',
                        message=f'High memory usage: {metrics.memory_percent:.1f}%',
                        value=metrics.memory_percent,
                        threshold=self.thresholds['memory_warning'],
                        recommendation='Monitor memory usage and consider cleanup or scaling'
                    ))
            
            # Disk alerts
            if metrics.disk_usage_percent >= self.thresholds['disk_critical']:
                if self._should_send_alert('disk_critical', current_time):
                    alerts.append(PerformanceAlert(
                        timestamp=datetime.now(),
                        level='critical',
                        category='disk',
                        message=f'Critical disk usage: {metrics.disk_usage_percent:.1f}%',
                        value=metrics.disk_usage_percent,
                        threshold=self.thresholds['disk_critical'],
                        recommendation='Immediate cleanup required or add more storage'
                    ))
            elif metrics.disk_usage_percent >= self.thresholds['disk_warning']:
                if self._should_send_alert('disk_warning', current_time):
                    alerts.append(PerformanceAlert(
                        timestamp=datetime.now(),
                        level='warning',
                        category='disk',
                        message=f'High disk usage: {metrics.disk_usage_percent:.1f}%',
                        value=metrics.disk_usage_percent,
                        threshold=self.thresholds['disk_warning'],
                        recommendation='Plan for disk cleanup or storage expansion'
                    ))
            
            # GPU alerts (if available)
            if metrics.gpu_usage is not None:
                if metrics.gpu_usage >= self.thresholds['gpu_critical']:
                    if self._should_send_alert('gpu_critical', current_time):
                        alerts.append(PerformanceAlert(
                            timestamp=datetime.now(),
                            level='critical',
                            category='gpu',
                            message=f'Critical GPU usage: {metrics.gpu_usage:.1f}%',
                            value=metrics.gpu_usage,
                            threshold=self.thresholds['gpu_critical'],
                            recommendation='GPU overloaded - consider reducing concurrent operations'
                        ))
                elif metrics.gpu_usage >= self.thresholds['gpu_warning']:
                    if self._should_send_alert('gpu_warning', current_time):
                        alerts.append(PerformanceAlert(
                            timestamp=datetime.now(),
                            level='warning',
                            category='gpu',
                            message=f'High GPU usage: {metrics.gpu_usage:.1f}%',
                            value=metrics.gpu_usage,
                            threshold=self.thresholds['gpu_warning'],
                            recommendation='Monitor GPU usage for sustained high load'
                        ))
            
            # Add alerts to history
            for alert in alerts:
                self.alerts_history.append(alert)
                self.stats['total_alerts'] += 1
                if alert.level == 'critical':
                    self.stats['critical_alerts'] += 1
                
                logger.warning(f"Performance Alert [{alert.level.upper()}]: {alert.message}")
                
        except Exception as e:
            logger.error(f"Failed to check alerts: {e}")
    
    def _should_send_alert(self, alert_key: str, current_time: float) -> bool:
        """Check if enough time has passed since last alert of this type"""
        last_alert_time = self.alert_cooldown.get(alert_key, 0)
        if current_time - last_alert_time >= self.alert_cooldown_period:
            self.alert_cooldown[alert_key] = current_time
            return True
        return False
    
    def _update_statistics(self, metrics: SystemMetrics):
        """Update performance statistics"""
        try:
            # Update averages
            if self.system_metrics_history:
                cpu_values = [m.cpu_percent for m in self.system_metrics_history]
                memory_values = [m.memory_percent for m in self.system_metrics_history]
                
                self.stats['average_cpu'] = sum(cpu_values) / len(cpu_values)
                self.stats['average_memory'] = sum(memory_values) / len(memory_values)
                self.stats['peak_cpu'] = max(cpu_values)
                self.stats['peak_memory'] = max(memory_values)
            
            # Update uptime
            if self.stats.get('monitoring_start_time'):
                uptime = datetime.now() - self.stats['monitoring_start_time']
                self.stats['uptime_hours'] = uptime.total_seconds() / 3600
                
        except Exception as e:
            logger.error(f"Failed to update statistics: {e}")
    
    async def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            system_metrics = self._collect_system_metrics()
            process_metrics = self._collect_process_metrics()
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'system': asdict(system_metrics) if system_metrics else None,
                'process': asdict(process_metrics) if process_metrics else None
            }
            
            # Convert datetime objects to strings
            if result['system']:
                result['system']['timestamp'] = system_metrics.timestamp.isoformat()
            if result['process']:
                result['process']['timestamp'] = process_metrics.timestamp.isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get current metrics: {e}")
            return {}
    
    async def get_metrics_history(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics history for specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter system metrics
            system_metrics = [
                {**asdict(m), 'timestamp': m.timestamp.isoformat()}
                for m in self.system_metrics_history
                if m.timestamp >= cutoff_time
            ]
            
            # Filter process metrics
            process_metrics = [
                {**asdict(m), 'timestamp': m.timestamp.isoformat()}
                for m in self.process_metrics_history
                if m.timestamp >= cutoff_time
            ]
            
            return {
                'system_metrics': system_metrics,
                'process_metrics': process_metrics,
                'period_hours': hours,
                'total_points': len(system_metrics)
            }
            
        except Exception as e:
            logger.error(f"Failed to get metrics history: {e}")
            return {}
    
    async def get_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get alerts for specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            alerts = [
                {**asdict(alert), 'timestamp': alert.timestamp.isoformat()}
                for alert in self.alerts_history
                if alert.timestamp >= cutoff_time
            ]
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get alerts: {e}")
            return []
    
    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        try:
            stats = dict(self.stats)
            
            # Convert datetime to string
            if stats.get('monitoring_start_time'):
                stats['monitoring_start_time'] = stats['monitoring_start_time'].isoformat()
            
            # Add current status
            stats.update({
                'is_monitoring': self.is_monitoring,
                'monitoring_interval': self.monitoring_interval,
                'history_size': len(self.system_metrics_history),
                'recent_alerts': len([
                    a for a in self.alerts_history
                    if a.timestamp >= datetime.now() - timedelta(hours=1)
                ])
            })
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get performance stats: {e}")
            return {}
    
    async def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get performance optimization recommendations"""
        try:
            recommendations = []
            
            if not self.system_metrics_history:
                return recommendations
            
            # Get recent metrics (last hour)
            recent_time = datetime.now() - timedelta(hours=1)
            recent_metrics = [
                m for m in self.system_metrics_history
                if m.timestamp >= recent_time
            ]
            
            if not recent_metrics:
                return recommendations
            
            # CPU recommendations
            avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
            if avg_cpu > 70:
                recommendations.append({
                    'category': 'cpu',
                    'priority': 'high' if avg_cpu > 85 else 'medium',
                    'title': 'High CPU Usage Detected',
                    'description': f'Average CPU usage is {avg_cpu:.1f}% over the last hour',
                    'recommendations': [
                        'Consider implementing CPU-intensive task queuing',
                        'Optimize video processing algorithms',
                        'Scale horizontally with more worker instances',
                        'Review and optimize database queries'
                    ]
                })
            
            # Memory recommendations
            avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
            if avg_memory > 75:
                recommendations.append({
                    'category': 'memory',
                    'priority': 'high' if avg_memory > 90 else 'medium',
                    'title': 'High Memory Usage Detected',
                    'description': f'Average memory usage is {avg_memory:.1f}% over the last hour',
                    'recommendations': [
                        'Implement memory caching with TTL',
                        'Add garbage collection optimization',
                        'Consider increasing available RAM',
                        'Review memory leaks in long-running processes'
                    ]
                })
            
            # Disk recommendations
            latest_disk = recent_metrics[-1].disk_usage_percent
            if latest_disk > 80:
                recommendations.append({
                    'category': 'disk',
                    'priority': 'high' if latest_disk > 95 else 'medium',
                    'title': 'High Disk Usage Detected',
                    'description': f'Disk usage is {latest_disk:.1f}%',
                    'recommendations': [
                        'Implement automatic cleanup of old files',
                        'Add file compression for stored media',
                        'Consider cloud storage for media files',
                        'Set up log rotation policies'
                    ]
                })
            
            # GPU recommendations (if available)
            gpu_metrics = [m for m in recent_metrics if m.gpu_usage is not None]
            if gpu_metrics:
                avg_gpu = sum(m.gpu_usage for m in gpu_metrics) / len(gpu_metrics)
                if avg_gpu > 80:
                    recommendations.append({
                        'category': 'gpu',
                        'priority': 'high' if avg_gpu > 95 else 'medium',
                        'title': 'High GPU Usage Detected',
                        'description': f'Average GPU usage is {avg_gpu:.1f}% over the last hour',
                        'recommendations': [
                            'Implement GPU task queuing',
                            'Optimize video processing batch sizes',
                            'Consider multiple GPU setup',
                            'Review GPU memory management'
                        ]
                    })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get optimization recommendations: {e}")
            return []
    
    async def trigger_cleanup(self) -> Dict[str, Any]:
        """Trigger system cleanup operations"""
        try:
            cleanup_results = {
                'timestamp': datetime.now().isoformat(),
                'operations': []
            }
            
            # Python garbage collection
            collected = gc.collect()
            cleanup_results['operations'].append({
                'operation': 'garbage_collection',
                'result': f'Collected {collected} objects',
                'success': True
            })
            
            # Clear old cache files
            try:
                cache_dirs = ['cache', 'temp', 'outputs']
                total_freed = 0
                
                for cache_dir in cache_dirs:
                    if os.path.exists(cache_dir):
                        for root, dirs, files in os.walk(cache_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    # Remove files older than 24 hours
                                    if os.path.getmtime(file_path) < time.time() - 86400:
                                        file_size = os.path.getsize(file_path)
                                        os.remove(file_path)
                                        total_freed += file_size
                                except Exception:
                                    pass
                
                cleanup_results['operations'].append({
                    'operation': 'cache_cleanup',
                    'result': f'Freed {total_freed / (1024**2):.1f} MB',
                    'success': True
                })
                
            except Exception as e:
                cleanup_results['operations'].append({
                    'operation': 'cache_cleanup',
                    'result': f'Failed: {str(e)}',
                    'success': False
                })
            
            return cleanup_results
            
        except Exception as e:
            logger.error(f"Cleanup operation failed: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'operations': [{
                    'operation': 'cleanup',
                    'result': f'Failed: {str(e)}',
                    'success': False
                }]
            }
    
    async def optimize_memory_usage(self) -> Dict[str, Any]:
        """Advanced memory optimization"""
        try:
            optimization_results = {
                'timestamp': datetime.now().isoformat(),
                'operations': [],
                'memory_before': 0.0,
                'memory_after': 0.0,
                'memory_freed_mb': 0.0
            }
            
            # Get memory before optimization
            memory_before = psutil.virtual_memory()
            optimization_results['memory_before'] = memory_before.percent
            
            # 1. Force garbage collection multiple times
            collected_total = 0
            for i in range(3):
                collected = gc.collect()
                collected_total += collected
                await asyncio.sleep(0.1)  # Small delay between collections
            
            optimization_results['operations'].append({
                'operation': 'garbage_collection',
                'result': f'Collected {collected_total} objects in 3 passes',
                'success': True
            })
            
            # 2. Clear Python caches
            try:
                import sys
                if hasattr(sys, '_clear_type_cache'):
                    sys._clear_type_cache()
                optimization_results['operations'].append({
                    'operation': 'clear_type_cache',
                    'result': 'Python type cache cleared',
                    'success': True
                })
            except Exception as e:
                optimization_results['operations'].append({
                    'operation': 'clear_type_cache',
                    'result': f'Failed: {str(e)}',
                    'success': False
                })
            
            # 3. Reduce monitoring history if too large
            if len(self.system_metrics_history) > 500:
                old_size = len(self.system_metrics_history)
                # Keep only last 300 entries
                while len(self.system_metrics_history) > 300:
                    self.system_metrics_history.popleft()
                
                optimization_results['operations'].append({
                    'operation': 'reduce_metrics_history',
                    'result': f'Reduced from {old_size} to {len(self.system_metrics_history)} entries',
                    'success': True
                })
            
            # 4. Clear old process metrics
            if len(self.process_metrics_history) > 500:
                old_size = len(self.process_metrics_history)
                while len(self.process_metrics_history) > 300:
                    self.process_metrics_history.popleft()
                
                optimization_results['operations'].append({
                    'operation': 'reduce_process_history',
                    'result': f'Reduced from {old_size} to {len(self.process_metrics_history)} entries',
                    'success': True
                })
            
            # Get memory after optimization
            await asyncio.sleep(1)  # Wait for changes to take effect
            memory_after = psutil.virtual_memory()
            optimization_results['memory_after'] = memory_after.percent
            
            # Calculate memory freed
            memory_freed_mb = (memory_before.used - memory_after.used) / (1024**2)
            optimization_results['memory_freed_mb'] = memory_freed_mb
            
            logger.info(f"Memory optimization completed. Freed: {memory_freed_mb:.1f} MB")
            
            return optimization_results
            
        except Exception as e:
            logger.error(f"Memory optimization failed: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'operations': [{
                    'operation': 'memory_optimization',
                    'result': f'Failed: {str(e)}',
                    'success': False
                }],
                'memory_before': 0.0,
                'memory_after': 0.0,
                'memory_freed_mb': 0.0
            }

    def __del__(self):
        """Cleanup when monitor is destroyed"""
        self.stop_monitoring()