"""
Performance Monitoring API Routes
Provides endpoints for system performance monitoring and optimization
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from services.performance_service import PerformanceMonitor

# Configure logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/performance", tags=["performance"])

# Initialize performance monitor (singleton)
performance_monitor = None

def get_performance_monitor():
    """Get performance monitor instance"""
    global performance_monitor
    if performance_monitor is None:
        performance_monitor = PerformanceMonitor()
    return performance_monitor

# Pydantic models for responses

class SystemMetricsResponse(BaseModel):
    """System metrics response"""
    timestamp: str
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

class ProcessMetricsResponse(BaseModel):
    """Process metrics response"""
    timestamp: str
    process_name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    threads: int
    status: str
    duration: float

class CurrentMetricsResponse(BaseModel):
    """Current metrics response"""
    timestamp: str
    system: Optional[SystemMetricsResponse]
    process: Optional[ProcessMetricsResponse]

class AlertResponse(BaseModel):
    """Performance alert response"""
    timestamp: str
    level: str
    category: str
    message: str
    value: float
    threshold: float
    recommendation: str

class PerformanceStatsResponse(BaseModel):
    """Performance statistics response"""
    monitoring_start_time: Optional[str]
    total_alerts: int
    critical_alerts: int
    average_cpu: float
    average_memory: float
    peak_cpu: float
    peak_memory: float
    uptime_hours: float
    is_monitoring: bool
    monitoring_interval: float
    history_size: int
    recent_alerts: int

class OptimizationRecommendation(BaseModel):
    """Optimization recommendation"""
    category: str
    priority: str
    title: str
    description: str
    recommendations: List[str]

class CleanupOperation(BaseModel):
    """Cleanup operation result"""
    operation: str
    result: str
    success: bool

class CleanupResponse(BaseModel):
    """Cleanup response"""
    timestamp: str
    operations: List[CleanupOperation]

class MemoryOptimizationResponse(BaseModel):
    """Memory optimization response"""
    timestamp: str
    operations: List[CleanupOperation]
    memory_before: float
    memory_after: float
    memory_freed_mb: float

# API Endpoints

@router.get("/current", response_model=CurrentMetricsResponse)
async def get_current_metrics(
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Get current system and process metrics
    
    Returns real-time performance metrics including:
    - CPU usage
    - Memory usage
    - Disk usage
    - GPU usage (if available)
    - Network activity
    - Process information
    """
    try:
        metrics = await monitor.get_current_metrics()
        
        # Convert to response format
        system_metrics = None
        if metrics.get('system'):
            system_metrics = SystemMetricsResponse(**metrics['system'])
        
        process_metrics = None
        if metrics.get('process'):
            process_metrics = ProcessMetricsResponse(**metrics['process'])
        
        return CurrentMetricsResponse(
            timestamp=metrics['timestamp'],
            system=system_metrics,
            process=process_metrics
        )
        
    except Exception as e:
        logger.error(f"Failed to get current metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get current metrics: {str(e)}")

@router.get("/history")
async def get_metrics_history(
    hours: int = Query(24, ge=1, le=168, description="Number of hours of history to retrieve"),
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Get historical performance metrics
    
    Returns performance metrics history for the specified time period.
    Useful for creating performance charts and trend analysis.
    """
    try:
        history = await monitor.get_metrics_history(hours=hours)
        return history
        
    except Exception as e:
        logger.error(f"Failed to get metrics history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get metrics history: {str(e)}")

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(
    hours: int = Query(24, ge=1, le=168, description="Number of hours of alerts to retrieve"),
    level: Optional[str] = Query(None, description="Filter by alert level (warning/critical)"),
    category: Optional[str] = Query(None, description="Filter by category (cpu/memory/disk/gpu)"),
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Get performance alerts
    
    Returns performance alerts for the specified time period.
    Alerts are generated when system metrics exceed configured thresholds.
    """
    try:
        alerts = await monitor.get_alerts(hours=hours)
        
        # Apply filters
        if level:
            alerts = [a for a in alerts if a['level'] == level.lower()]
        
        if category:
            alerts = [a for a in alerts if a['category'] == category.lower()]
        
        # Convert to response format
        alert_responses = [AlertResponse(**alert) for alert in alerts]
        
        return alert_responses
        
    except Exception as e:
        logger.error(f"Failed to get alerts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get alerts: {str(e)}")

@router.get("/stats", response_model=PerformanceStatsResponse)
async def get_performance_stats(
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Get performance statistics
    
    Returns overall performance statistics including:
    - Monitoring uptime
    - Alert counts
    - Average and peak resource usage
    - System health indicators
    """
    try:
        stats = await monitor.get_performance_stats()
        return PerformanceStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Failed to get performance stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get performance stats: {str(e)}")

@router.get("/recommendations", response_model=List[OptimizationRecommendation])
async def get_optimization_recommendations(
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Get optimization recommendations
    
    Analyzes recent performance data and provides actionable recommendations
    for improving system performance and resource utilization.
    """
    try:
        recommendations = await monitor.get_optimization_recommendations()
        return [OptimizationRecommendation(**rec) for rec in recommendations]
        
    except Exception as e:
        logger.error(f"Failed to get optimization recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get optimization recommendations: {str(e)}")

@router.post("/cleanup", response_model=CleanupResponse)
async def trigger_cleanup(
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Trigger system cleanup operations
    
    Performs various cleanup operations to free up system resources:
    - Python garbage collection
    - Cache file cleanup
    - Temporary file removal
    - Memory optimization
    """
    try:
        cleanup_result = await monitor.trigger_cleanup()
        
        # Convert to response format
        operations = [CleanupOperation(**op) for op in cleanup_result['operations']]
        
        return CleanupResponse(
            timestamp=cleanup_result['timestamp'],
            operations=operations
        )
        
    except Exception as e:
        logger.error(f"Failed to trigger cleanup: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger cleanup: {str(e)}")

@router.get("/health")
async def performance_health_check(
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Performance monitoring health check
    
    Returns the health status of the performance monitoring system.
    """
    try:
        current_metrics = await monitor.get_current_metrics()
        stats = await monitor.get_performance_stats()
        
        # Determine health status
        is_healthy = True
        issues = []
        
        if current_metrics.get('system'):
            system = current_metrics['system']
            
            # Check critical thresholds
            if system.get('cpu_percent', 0) > 95:
                is_healthy = False
                issues.append("Critical CPU usage")
            
            if system.get('memory_percent', 0) > 95:
                is_healthy = False
                issues.append("Critical memory usage")
            
            if system.get('disk_usage_percent', 0) > 98:
                is_healthy = False
                issues.append("Critical disk usage")
        
        # Check monitoring status
        if not stats.get('is_monitoring', False):
            is_healthy = False
            issues.append("Performance monitoring not active")
        
        # Check recent alerts
        recent_critical_alerts = stats.get('recent_alerts', 0)
        if recent_critical_alerts > 5:
            is_healthy = False
            issues.append(f"High number of recent alerts: {recent_critical_alerts}")
        
        return {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'is_monitoring': stats.get('is_monitoring', False),
            'issues': issues,
            'uptime_hours': stats.get('uptime_hours', 0),
            'total_alerts': stats.get('total_alerts', 0),
            'critical_alerts': stats.get('critical_alerts', 0),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Performance health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

@router.get("/summary")
async def get_performance_summary(
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Get performance summary
    
    Returns a comprehensive summary of system performance including
    current metrics, recent trends, and key indicators.
    """
    try:
        # Get current metrics
        current = await monitor.get_current_metrics()
        
        # Get recent history (last 4 hours)
        history = await monitor.get_metrics_history(hours=4)
        
        # Get recent alerts
        alerts = await monitor.get_alerts(hours=24)
        
        # Get stats
        stats = await monitor.get_performance_stats()
        
        # Calculate trends
        trends = {}
        if history.get('system_metrics'):
            metrics = history['system_metrics']
            if len(metrics) >= 2:
                # Calculate average for first and second half
                mid_point = len(metrics) // 2
                first_half = metrics[:mid_point]
                second_half = metrics[mid_point:]
                
                if first_half and second_half:
                    first_avg_cpu = sum(m['cpu_percent'] for m in first_half) / len(first_half)
                    second_avg_cpu = sum(m['cpu_percent'] for m in second_half) / len(second_half)
                    trends['cpu_trend'] = 'increasing' if second_avg_cpu > first_avg_cpu else 'decreasing'
                    
                    first_avg_memory = sum(m['memory_percent'] for m in first_half) / len(first_half)
                    second_avg_memory = sum(m['memory_percent'] for m in second_half) / len(second_half)
                    trends['memory_trend'] = 'increasing' if second_avg_memory > first_avg_memory else 'decreasing'
        
        # Count alerts by level
        alert_counts = {
            'warning': len([a for a in alerts if a['level'] == 'warning']),
            'critical': len([a for a in alerts if a['level'] == 'critical'])
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'current_metrics': current,
            'trends': trends,
            'alert_counts': alert_counts,
            'performance_stats': stats,
            'health_status': 'healthy' if alert_counts['critical'] == 0 else 'warning' if alert_counts['critical'] < 3 else 'critical'
        }
        
    except Exception as e:
        logger.error(f"Failed to get performance summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get performance summary: {str(e)}")

@router.get("/system-info")
async def get_system_info():
    """
    Get system information
    
    Returns static system information including hardware specs,
    OS details, and available resources.
    """
    try:
        import platform
        import psutil
        
        # Get system information
        system_info = {
            'platform': {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'architecture': platform.architecture(),
                'hostname': platform.node()
            },
            'cpu': {
                'physical_cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True),
                'max_frequency': psutil.cpu_freq().max if psutil.cpu_freq() else None,
                'current_frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None
            },
            'memory': {
                'total_gb': psutil.virtual_memory().total / (1024**3),
                'available_gb': psutil.virtual_memory().available / (1024**3)
            },
            'disk': {
                'total_gb': psutil.disk_usage('/').total / (1024**3),
                'free_gb': psutil.disk_usage('/').free / (1024**3)
            },
            'network': {
                'interfaces': list(psutil.net_if_addrs().keys())
            }
        }
        
        # Add GPU information if available
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_info = []
                for gpu in gpus:
                    gpu_info.append({
                        'id': gpu.id,
                        'name': gpu.name,
                        'memory_total_gb': gpu.memoryTotal / 1024,
                        'driver_version': gpu.driver
                    })
                system_info['gpu'] = gpu_info
        except Exception:
            system_info['gpu'] = None
        
        return system_info
        
    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get system info: {str(e)}")

@router.post("/optimize-memory", response_model=MemoryOptimizationResponse)
async def optimize_memory(
    monitor: PerformanceMonitor = Depends(get_performance_monitor)
):
    """
    Optimize memory usage
    
    Performs advanced memory optimization including:
    - Garbage collection
    - Cache clearing
    - History reduction
    - Python type cache clearing
    
    Returns detailed information about the optimization process
    and memory freed.
    """
    try:
        result = await monitor.optimize_memory_usage()
        
        # Convert operations to response format
        operations = [
            CleanupOperation(**op) for op in result['operations']
        ]
        
        return MemoryOptimizationResponse(
            timestamp=result['timestamp'],
            operations=operations,
            memory_before=result['memory_before'],
            memory_after=result['memory_after'],
            memory_freed_mb=result['memory_freed_mb']
        )
        
    except Exception as e:
        logger.error(f"Failed to optimize memory: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to optimize memory: {str(e)}")