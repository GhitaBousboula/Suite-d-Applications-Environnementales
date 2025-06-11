<<<<<<< HEAD
    # Enhanced Google Earth Engine Authentication Module
    # Service Account + Rectangle ROI + Delta VV Maps with Geemap - ENHANCED LOCAL VISUALIZATION

import streamlit as st
import geemap.foliumap as geemap
import ee
import json
import os
import tempfile
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from google.oauth2 import service_account
import traceback
from typing import Optional, Dict, Any, List
import numpy as np
import calendar

def run():
    st.title("🛰️ Monitoring de phase construction en utilisant la télédétection")





    class SimplifiedGEEAuth:
        """Simplified Google Earth Engine Authentication - Service Account Only"""
        
        def __init__(self):
            self.authenticated = False
            self.credentials = None
            
        def authenticate(self) -> bool:
            """Service Account authentication only"""
            st.subheader("🔐 Google Earth Engine Authentication")
            
            # Check if already authenticated
            if self.check_existing_auth():
                return True
            
            # Show service account upload interface
            return self.auth_with_file_upload()
        
        def check_existing_auth(self) -> bool:
            """Check if GEE is already authenticated"""
            try:
                test_result = ee.Number(1).getInfo()
                if test_result == 1:
                    st.success("✅ Google Earth Engine already authenticated!")
                    self.authenticated = True
                    return True
            except Exception:
                pass
            return False
        
        def auth_with_file_upload(self) -> bool:
            """Authentication via service account file upload"""
            
            st.markdown("### 📤 Upload Service Account JSON File")
            
            with st.expander("📋 How to get a Service Account file", expanded=False):
                st.markdown("""
                **Steps to create a Service Account:**
                1. Go to [Google Cloud Console](https://console.cloud.google.com/)
                2. Create or select a project
                3. Enable the Earth Engine API
                4. Go to IAM & Admin > Service Accounts
                5. Create a new service account
                6. Download the JSON key file
                7. Upload it below
                """)
            
            uploaded_file = st.file_uploader(
                "Select your service account JSON file:",
                type=['json'],
                help="Upload the service account key file downloaded from Google Cloud Console"
            )
            
            if uploaded_file is not None:
                if st.button("🔐 Authenticate", key="auth_button"):
                    return self.process_uploaded_file(uploaded_file)
            
            return False
        
        def process_uploaded_file(self, uploaded_file) -> bool:
            """Process the uploaded service account file"""
            try:
                file_content = uploaded_file.read()
                uploaded_file.seek(0)
                
                try:
                    credentials_dict = json.loads(file_content)
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON file: {str(e)}")
                    return False
                
                # Validate service account structure
                required_fields = ['type', 'project_id', 'private_key', 'client_email']
                missing_fields = [field for field in required_fields if field not in credentials_dict]
                
                if missing_fields:
                    st.error(f"❌ Missing required fields: {', '.join(missing_fields)}")
                    return False
                
                if credentials_dict.get('type') != 'service_account':
                    st.error("❌ File is not a valid service account")
                    return False
                
                # Create temporary file for authentication
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                    json.dump(credentials_dict, temp_file, indent=2)
                    temp_file_path = temp_file.name
                
                try:
                    credentials = service_account.Credentials.from_service_account_file(
                        temp_file_path,
                        scopes=['https://www.googleapis.com/auth/earthengine']
                    )
                    
                    ee.Initialize(credentials)
                    
                    # Test authentication
                    test_result = ee.Number(42).getInfo()
                    
                    if test_result == 42:
                        st.success("✅ Authentication successful!")
                        st.success(f"🎯 Project: {credentials_dict.get('project_id', 'Unknown')}")
                        st.success(f"📧 Service Account: {credentials_dict.get('client_email', 'Unknown')}")
                        
                        self.authenticated = True
                        self.credentials = credentials
                        
                        # Store in session state
                        st.session_state.gee_credentials = credentials_dict
                        st.session_state.gee_authenticated = True
                        
                        return True
                    else:
                        st.error("❌ Authentication test failed")
                        return False
                        
                except Exception as e:
                    st.error(f"❌ Authentication failed: {str(e)}")
                    return False
                
                finally:
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
            
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                return False
        
        def is_authenticated(self) -> bool:
            """Check if currently authenticated"""
            if not self.authenticated:
                return False
            
            try:
                ee.Number(1).getInfo()
                return True
            except:
                self.authenticated = False
                return False


    class GEEGeomapAnalyzer:
        """GEE Analyzer using Geemap for Delta VV visualization - ENHANCED LOCAL CHANGES"""
        
        def __init__(self):
            self.auth_manager = SimplifiedGEEAuth()
            # Enhanced palettes for better local visualization
            self.palette_fine = ['#000080', '#0000FF', '#4169E1', '#87CEEB', '#FFFFFF', '#FFB6C1', '#FF4500', '#FF0000', '#8B0000']
            self.palette_coarse = ['#0000FF', '#FFFFFF', '#FF0000']
            
            # Multiple visualization parameter sets
            self.vis_params_adaptive = {'min': -0.02, 'max': 0.02, 'palette': self.palette_fine}
            self.vis_params_sensitive = {'min': -0.01, 'max': 0.01, 'palette': self.palette_fine}
            self.vis_params_robust = {'min': -0.05, 'max': 0.05, 'palette': self.palette_fine}
            
        def ensure_authentication(self) -> bool:
            """Ensure GEE is authenticated"""
            if self.auth_manager.is_authenticated():
                return True
            
            st.warning("⚠️ Google Earth Engine authentication required")
            return self.auth_manager.authenticate()
            
        def preprocess_s1(self, img, roi):
            """Enhanced Sentinel-1 preprocessing with noise reduction - FIXED VERSION"""
            try:
                # Get VV band
                vv = img.select('VV')
                
                # Convert to dB and scale
                vv_db = vv.multiply(0.0001)
                
                # Apply speckle filtering using focal_mean with radius parameter
                # Use a numeric radius instead of kernel for focal_mean
                vv_filtered = vv_db.focal_mean(radius=1.5, kernelType='square', units='pixels')
                
                # Alternative approach using convolve if you prefer kernel-based filtering:
                # kernel = ee.Kernel.square(1.5, 'pixels', False)
                # vv_filtered = vv_db.convolve(kernel.normalize())
                
                # Clip to ROI
                vv_clipped = vv_filtered.clip(roi)
                
                return vv_clipped.copyProperties(img, ["system:time_start"])
                
            except Exception as e:
                st.error(f"❌ Error preprocessing Sentinel-1: {e}")
                return None
        
        def get_monthly_delta_enhanced(self, year: int, month: int, reference_img, roi):
            """Enhanced monthly delta calculation with better statistics"""
            try:
                # Create start and end dates for the month
                start = ee.Date(f"{year}-{month:02d}-01")
                end = start.advance(1, 'month')
                
                # Get monthly collection with more strict filtering
                monthly_collection = ee.ImageCollection("COPERNICUS/S1_GRD") \
                    .filterBounds(roi) \
                    .filterDate(start, end) \
                    .filter(ee.Filter.eq('instrumentMode', 'IW')) \
                    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
                    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))  # Use only descending passes for consistency
                
                # Check if we have data
                size = monthly_collection.size().getInfo()
                if size == 0:
                    return None, None
                
                # Process images and get median
                processed_collection = monthly_collection.map(lambda img: self.preprocess_s1(img, roi))
                monthly_median = processed_collection.median()
                
                # Calculate delta
                delta = monthly_median.subtract(reference_img).rename(f'delta_VV_{year}_{month:02d}')
                
                # Calculate local statistics for adaptive visualization
                local_stats = delta.reduceRegion(
                    reducer=ee.Reducer.percentile([5, 25, 50, 75, 95]),
                    geometry=roi,
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                delta_with_props = delta.set({
                    'year': year, 
                    'month': month,
                    'image_count': size,
                    'p5': local_stats.get(f'delta_VV_{year}_{month:02d}_p5', -0.02),
                    'p25': local_stats.get(f'delta_VV_{year}_{month:02d}_p25', -0.01),
                    'p50': local_stats.get(f'delta_VV_{year}_{month:02d}_p50', 0),
                    'p75': local_stats.get(f'delta_VV_{year}_{month:02d}_p75', 0.01),
                    'p95': local_stats.get(f'delta_VV_{year}_{month:02d}_p95', 0.02)
                })
                
                return delta_with_props, local_stats
                
            except Exception as e:
                st.warning(f"⚠️ Error calculating monthly delta for {year}-{month:02d}: {e}")
                return None, None
        
        def create_reference_image_enhanced(self, roi, ref_start: str, ref_end: str):
            """Enhanced reference image creation"""
            try:
                st.info(f"🔍 Creating enhanced reference image for period: {ref_start} to {ref_end}")
                
                ref_collection = ee.ImageCollection("COPERNICUS/S1_GRD") \
                    .filterBounds(roi) \
                    .filterDate(ref_start, ref_end) \
                    .filter(ee.Filter.eq('instrumentMode', 'IW')) \
                    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
                    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
                
                size = ref_collection.size().getInfo()
                if size == 0:
                    st.error(f"❌ No Sentinel-1 images found for reference period")
                    return None
                
                st.success(f"✅ Found {size} images for reference period")
                
                # Process reference images with enhanced filtering
                processed_ref = ref_collection.map(lambda img: self.preprocess_s1(img, roi))
                reference_img = processed_ref.median()
                
                return reference_img
                
            except Exception as e:
                st.error(f"❌ Error creating reference image: {e}")
                return None
        
        def create_rectangle_roi(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float):
            """Create rectangular ROI from coordinates"""
            try:
                roi = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])
                st.success(f"✅ Rectangle ROI created: ({lat_min}, {lon_min}) to ({lat_max}, {lon_max})")
                return roi
            except Exception as e:
                st.error(f"❌ Error creating rectangle ROI: {e}")
                return None
        
        def get_adaptive_vis_params(self, local_stats: Dict, sensitivity: str = "medium"):
            """Get adaptive visualization parameters based on local statistics"""
            try:
                if not local_stats:
                    return self.vis_params_adaptive
                
                # Extract percentiles
                p5 = local_stats.get('p5', -0.02)
                p95 = local_stats.get('p95', 0.02)
                p25 = local_stats.get('p25', -0.01)
                p75 = local_stats.get('p75', 0.01)
                
                if sensitivity == "high":
                    # Use 25th-75th percentiles for high sensitivity
                    min_val = max(p25, -0.03)
                    max_val = min(p75, 0.03)
                elif sensitivity == "low":
                    # Use 5th-95th percentiles for low sensitivity
                    min_val = max(p5, -0.05)
                    max_val = min(p95, 0.05)
                else:  # medium
                    # Use adaptive range
                    range_val = max(abs(p5), abs(p95))
                    min_val = max(-range_val, -0.04)
                    max_val = min(range_val, 0.04)
                
                return {
                    'min': min_val,
                    'max': max_val,
                    'palette': self.palette_fine
                }
                
            except Exception as e:
                st.warning(f"⚠️ Error calculating adaptive parameters: {e}")
                return self.vis_params_adaptive
        
        def analyze_delta_vv_enhanced(self, lat_min: float, lat_max: float, 
                                    lon_min: float, lon_max: float,
                                    start_year: int, end_year: int,
                                    start_month: int, end_month: int,
                                    ref_start: str, ref_end: str):
            """Enhanced main analysis function"""
            if not self.ensure_authentication():
                return [], [], None
            
            try:
                st.info("🛰️ Starting Enhanced Delta VV analysis...")
                
                # Create ROI
                roi = self.create_rectangle_roi(lat_min, lat_max, lon_min, lon_max)
                if roi is None:
                    return [], [], None
                
                # Create enhanced reference image
                reference_img = self.create_reference_image_enhanced(roi, ref_start, ref_end)
                if reference_img is None:
                    return [], [], None
                
                # Calculate Delta VV images with enhanced processing
                delta_images = []
                stats_data = []
                
                total_months = 0
                for year in range(start_year, end_year + 1):
                    for month in range(1, 13):
                        if year == start_year and month < start_month:
                            continue
                        if year == end_year and month > end_month:
                            break
                        total_months += 1
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                current_month = 0
                
                for year in range(start_year, end_year + 1):
                    for month in range(1, 13):
                        if year == start_year and month < start_month:
                            continue
                        if year == end_year and month > end_month:
                            break
                        
                        current_month += 1
                        progress = current_month / total_months
                        progress_bar.progress(progress)
                        status_text.text(f"Processing {calendar.month_abbr[month]} {year} ({current_month}/{total_months})")
                        
                        try:
                            delta_img, local_stats = self.get_monthly_delta_enhanced(year, month, reference_img, roi)
                            
                            if delta_img is not None and local_stats is not None:
                                # Calculate comprehensive statistics
                                stats = delta_img.reduceRegion(
                                    reducer=ee.Reducer.mean().combine(
                                        ee.Reducer.stdDev(), sharedInputs=True
                                    ).combine(
                                        ee.Reducer.minMax(), sharedInputs=True
                                    ).combine(
                                        ee.Reducer.percentile([10, 25, 50, 75, 90]), sharedInputs=True
                                    ),
                                    geometry=roi,
                                    scale=10,
                                    maxPixels=1e9
                                ).getInfo()
                                
                                if stats:
                                    delta_key = f'delta_VV_{year}_{month:02d}'
                                    stats_data.append({
                                        'date': f'{year}-{month:02d}-01',
                                        'year': year,
                                        'month': month,
                                        'month_name': calendar.month_abbr[month],
                                        'mean_delta': stats.get(f'{delta_key}_mean', 0),
                                        'std_delta': stats.get(f'{delta_key}_stdDev', 0),
                                        'min_delta': stats.get(f'{delta_key}_min', 0),
                                        'max_delta': stats.get(f'{delta_key}_max', 0),
                                        'p10': stats.get(f'{delta_key}_p10', 0),
                                        'p25': stats.get(f'{delta_key}_p25', 0),
                                        'p50': stats.get(f'{delta_key}_p50', 0),
                                        'p75': stats.get(f'{delta_key}_p75', 0),
                                        'p90': stats.get(f'{delta_key}_p90', 0),
                                        'image_count': delta_img.get('image_count').getInfo()
                                    })
                                    
                                    # Get adaptive visualization parameters
                                    adaptive_vis = self.get_adaptive_vis_params(local_stats, "medium")
                                    
                                    delta_images.append({
                                        'image': delta_img,
                                        'date': f'{calendar.month_abbr[month]} {year}',
                                        'year': year,
                                        'month': month,
                                        'label': f'ΔVV {calendar.month_abbr[month]} {year}',
                                        'local_stats': local_stats,
                                        'adaptive_vis': adaptive_vis
                                    })
                        
                        except Exception as e:
                            st.warning(f"⚠️ Error processing {calendar.month_abbr[month]} {year}: {e}")
                
                progress_bar.progress(1.0)
                status_text.text(f"✅ Enhanced analysis complete! Processed {len(stats_data)} months")
                
                return delta_images, stats_data, roi
                
            except Exception as e:
                st.error(f"❌ Error in enhanced analysis: {e}")
                return [], [], None
        
        def create_enhanced_geemap_visualization(self, delta_images: List, roi, selected_indices: List[int] = None, 
                                            sensitivity: str = "medium", vis_mode: str = "adaptive"):
            """Enhanced Geemap visualization with multiple visualization modes - ROI BOUNDARY REMOVED"""
            try:
                if not delta_images:
                    st.warning("⚠️ No delta images available for mapping")
                    return None
                
                # Get ROI coordinates for centering
                try:
                    roi_coords = roi.coordinates().getInfo()
                    if roi_coords and len(roi_coords) > 0 and len(roi_coords[0]) > 0:
                        coords = roi_coords[0]
                        center_lat = (coords[0][1] + coords[2][1]) / 2
                        center_lon = (coords[0][0] + coords[2][0]) / 2
                    else:
                        center_lat, center_lon = 33.575, -7.5875
                except Exception:
                    center_lat, center_lon = 33.575, -7.5875
                
                # Create Enhanced Geemap Map
                Map = geemap.Map(
                    center=[center_lat, center_lon],
                    zoom=15,  # Higher zoom for local details
                    height=700
                )
                
                # Add high-resolution satellite basemap
                Map.add_basemap('SATELLITE')
                
                # ROI BOUNDARY SECTION COMMENTED OUT - NO MORE RED RECTANGLE!
                # try:
                #     roi_feature = ee.Feature(roi, {'name': 'Study Area'})
                #     roi_collection = ee.FeatureCollection([roi_feature])
                #     
                #     Map.addLayer(roi_collection, {
                #         'color': '#FF0000',
                #         'width': 3,
                #         'fillColor': '00000000'  # Transparent fill
                #     }, "ROI Boundary", True, 1.0)
                #     
                #     st.success("✅ ROI boundary added")
                #     
                # except Exception as roi_error:
                #     st.warning(f"⚠️ Could not add ROI boundary: {roi_error}")
                
                # Add selected delta layers with enhanced visualization
                if selected_indices is None:
                    selected_indices = list(range(min(2, len(delta_images))))
                
                st.info(f"Adding {len(selected_indices)} enhanced delta VV layers...")
                
                added_layers = 0
                for i, idx in enumerate(selected_indices):
                    if idx < len(delta_images):
                        delta_data = delta_images[idx]
                        delta_img = delta_data['image']
                        label = delta_data['label']
                        
                        # Choose visualization parameters based on mode
                        if vis_mode == "adaptive" and 'adaptive_vis' in delta_data:
                            vis_params = delta_data['adaptive_vis']
                        elif vis_mode == "sensitive":
                            vis_params = self.vis_params_sensitive
                        elif vis_mode == "robust":
                            vis_params = self.vis_params_robust
                        else:  # standard
                            vis_params = self.vis_params_adaptive
                        
                        # Adjust sensitivity
                        if sensitivity == "high":
                            vis_params['min'] = vis_params['min'] * 0.5
                            vis_params['max'] = vis_params['max'] * 0.5
                        elif sensitivity == "low":
                            vis_params['min'] = vis_params['min'] * 2
                            vis_params['max'] = vis_params['max'] * 2
                        
                        try:
                            Map.addLayer(
                                delta_img,
                                vis_params,
                                f"{label} ({vis_mode})",
                                True,
                                0.8
                            )
                            added_layers += 1
                            st.success(f"✅ Added: {label} (range: {vis_params['min']:.3f} to {vis_params['max']:.3f})")
                            
                        except Exception as layer_error:
                            st.error(f"❌ Failed to add {label}: {str(layer_error)}")
                            continue
                
                if added_layers == 0:
                    st.error("❌ No layers were successfully added")
                    return None
                
                # Add layer control
                Map.add_layer_control()
                
                # Add enhanced legend
                legend_dict = {
                    'Major Decrease (Construction)': '#000080',
                    'Moderate Decrease': '#0000FF', 
                    'Light Decrease': '#4169E1',
                    'Minimal Change': '#87CEEB',
                    'No Change': '#FFFFFF',
                    'Minimal Increase': '#FFB6C1',
                    'Light Increase': '#FF4500',
                    'Moderate Increase': '#FF0000',
                    'Major Increase (New Structures)': '#8B0000'
                }
                
                try:
                    Map.add_legend(legend_dict=legend_dict, title=f"Delta VV Changes ({vis_mode} mode)")
                except Exception:
                    pass
                
                st.success(f"✅ Enhanced map created with {added_layers} layers in {vis_mode} mode (ROI boundary hidden)")
                return Map
                
            except Exception as e:
                st.error(f"❌ Error creating enhanced map: {e}")
                return None
        
        def create_enhanced_time_series_plot(self, stats_data: List[Dict]):
            """Enhanced time series plot with percentiles"""
            try:
                df = pd.DataFrame(stats_data)
                
                fig = go.Figure()
                
                # Main time series
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['mean_delta'],
                    mode='lines+markers',
                    name='Mean Delta VV',
                    line=dict(color='blue', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{x}</b><br>Mean ΔVV: %{y:.4f}<extra></extra>'
                ))
                
                # Add percentile bands
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['p75'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['p25'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(0,100,80,0.2)',
                    name='25th-75th Percentile',
                    hoverinfo='skip'
                ))
                
                # Add median line
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['p50'],
                    mode='lines',
                    name='Median Delta VV',
                    line=dict(color='green', width=2, dash='dash'),
                    hovertemplate='<b>%{x}</b><br>Median ΔVV: %{y:.4f}<extra></extra>'
                ))
                
                fig.update_layout(
                    title='📈 Enhanced Evolution of Radar Backscatter Changes (Delta VV)',
                    xaxis_title='Date',
                    yaxis_title='Delta VV (dB)',
                    hovermode='x unified',
                    showlegend=True,
                    height=600
                )
                
                return fig
                
            except Exception as e:
                st.error(f"❌ Error creating enhanced plot: {e}")
                return None


    def create_enhanced_configuration_interface():
        """Enhanced configuration interface"""
        st.subheader("📍 Enhanced Study Area Configuration")
        
        # ROI Configuration
        st.markdown("#### Rectangle ROI Definition")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Southwest Corner (Bottom-left)**")
            lat_min = st.number_input("Latitude Min", value=33.5700, format="%.6f", key="lat_min")
            lon_min = st.number_input("Longitude Min", value=-7.5950, format="%.6f", key="lon_min")
        
        with col2:
            st.markdown("**Northeast Corner (Top-right)**")
            lat_max = st.number_input("Latitude Max", value=33.5800, format="%.6f", key="lat_max")
            lon_max = st.number_input("Longitude Max", value=-7.5800, format="%.6f", key="lon_max")
        
        # Validation
        if lat_min >= lat_max:
            st.error("❌ Latitude Min must be less than Latitude Max")
        if lon_min >= lon_max:
            st.error("❌ Longitude Min must be less than Longitude Max")
        
        # Calculate area
        lat_diff = lat_max - lat_min
        lon_diff = lon_max - lon_min
        area_km2 = lat_diff * lon_diff * 111 * 111 * np.cos(np.radians((lat_min + lat_max)/2))
        st.info(f"📏 Approximate area: {area_km2:.2f} km²")
        
        # Time Period Configuration
        st.markdown("#### Analysis Period")
        col1, col2 = st.columns(2)
        
        with col1:
            start_year = st.number_input("Start Year", value=2024, min_value=2020, max_value=2025)
            start_month = st.selectbox("Start Month", options=list(range(1, 13)), 
                                    format_func=lambda x: calendar.month_name[x], index=4)
        
        with col2:
            end_year = st.number_input("End Year", value=2025, min_value=2020, max_value=2025)
            end_month = st.selectbox("End Month", options=list(range(1, 13)), 
                                format_func=lambda x: calendar.month_name[x], index=5)
        
        # Reference Period
        st.markdown("#### Reference Period")
        st.info("Period before construction work for comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            ref_start = st.date_input("Reference Start", value=datetime(2024, 4, 1))
        with col2:
            ref_end = st.date_input("Reference End", value=datetime(2024, 5, 1))
        
        # Enhanced Visualization Options
        st.markdown("#### 🎨 Enhanced Visualization Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sensitivity = st.selectbox(
                "Sensitivity Level",
                options=["high", "medium", "low"],
                index=1,
                help="High: More sensitive to small changes, Low: Focus on larger changes"
            )
        
        with col2:
            vis_mode = st.selectbox(
                "Visualization Mode",
                options=["adaptive", "sensitive", "standard", "robust"],
                index=0,
                help="Adaptive: Auto-adjust based on data, Sensitive: Fixed high sensitivity"
            )
        
        with col3:
            filter_mode = st.selectbox(
                "Image Filtering",
                options=["enhanced", "standard"],
                index=0,
                help="Enhanced: Apply speckle filtering, Standard: Basic processing"
            )
        
        return (lat_min, lat_max, lon_min, lon_max, 
                start_year, end_year, start_month, end_month,
                ref_start.strftime('%Y-%m-%d'), ref_end.strftime('%Y-%m-%d'),
                sensitivity, vis_mode, filter_mode)



    def main():
        """Enhanced Main application - FIXED VERSION"""
        
        # Initialize analyzer
        if 'gee_analyzer' not in st.session_state:
            st.session_state.gee_analyzer = GEEGeomapAnalyzer()
        
        analyzer = st.session_state.gee_analyzer
        
        st.markdown("*Enhanced Delta VV Analysis and Visualization - ENHANCED LOCAL VISUALIZATION*")
        
        # Authentication section
        st.subheader("🔐 Authentication")
        
        if analyzer.auth_manager.is_authenticated():
            st.success("✅ Google Earth Engine authenticated!")
            
            if st.button("🔄 Re-authenticate"):
                analyzer.auth_manager.authenticated = False
                st.rerun()
        else:
            if not analyzer.ensure_authentication():
                st.stop()
        
        # Enhanced Configuration
        (lat_min, lat_max, lon_min, lon_max, 
        start_year, end_year, start_month, end_month,
        ref_start, ref_end, sensitivity, vis_mode, filter_mode) = create_enhanced_configuration_interface()

        # Validation before analysis
        if lat_min >= lat_max or lon_min >= lon_max:
            st.error("❌ Please correct the coordinate bounds before proceeding")
            st.stop()
        
        # Enhanced Analysis button
        if st.button("🚀 Launch Enhanced Delta VV Analysis", type="primary", use_container_width=True):
            with st.spinner("🛰️ Analyzing satellite data with enhanced processing..."):
                delta_images, stats_data, roi = analyzer.analyze_delta_vv_enhanced(
                    lat_min, lat_max, lon_min, lon_max,
                    start_year, end_year, start_month, end_month,
                    ref_start, ref_end
                )
                
                # Store results with enhanced config
                st.session_state.analysis_results = {
                    'delta_images': delta_images,
                    'stats_data': stats_data,
                    'roi': roi,
                    'config': {
                        'lat_min': lat_min, 'lat_max': lat_max,
                        'lon_min': lon_min, 'lon_max': lon_max,
                        'start_year': start_year, 'end_year': end_year,
                        'start_month': start_month, 'end_month': end_month,
                        'sensitivity': sensitivity,
                        'vis_mode': vis_mode,
                        'filter_mode': filter_mode
                    }
                }
                
                st.success("✅ Enhanced analysis completed!")
        
        # Enhanced Results section
        if 'analysis_results' in st.session_state:
            results = st.session_state.analysis_results
            
            if results['stats_data'] and results['delta_images']:
                st.subheader("📊 Enhanced Analysis Results")
                
                # Enhanced Time series plot
                st.markdown("### 📈 Enhanced Time Series Analysis")
                fig = analyzer.create_enhanced_time_series_plot(results['stats_data'])
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Enhanced Geemap visualization
                st.markdown("### 🗺️ Enhanced Interactive Delta VV Maps")
                st.info("💡 Enhanced visualization shows changes in radar backscatter with adaptive scaling. Blue = decrease (construction/disturbance), Red = increase (new structures)")
                
                # Enhanced Layer selection with visualization controls
                layer_options = [f"{img['label']}" for img in results['delta_images']]
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    selected_layers = st.multiselect(
                        "Select layers to display:",
                        options=layer_options,
                        default=layer_options[-2:] if len(layer_options) >= 2 else layer_options,
                        help="Select which months to display (max 3 for performance)"
                    )
                
                with col2:
                    # Get sensitivity and vis_mode from stored config or use defaults
                    current_sensitivity = results['config'].get('sensitivity', 'medium')
                    current_vis_mode = results['config'].get('vis_mode', 'adaptive')
                    
                    sensitivity_override = st.selectbox(
                        "Sensitivity:",
                        options=["high", "medium", "low"],
                        index=["high", "medium", "low"].index(current_sensitivity),
                        help="Override sensitivity for visualization"
                    )
                
                with col3:
                    vis_mode_override = st.selectbox(
                        "Viz Mode:",
                        options=["adaptive", "sensitive", "standard", "robust"],
                        index=["adaptive", "sensitive", "standard", "robust"].index(current_vis_mode),
                        help="Override visualization mode"
                    )
                
                # Quick selection buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔄 Latest 2", use_container_width=True):
                        st.session_state.selected_layers = layer_options[-2:] if len(layer_options) >= 2 else layer_options
                        st.rerun()
                with col2:
                    if st.button("📊 All Data", use_container_width=True):
                        st.session_state.selected_layers = layer_options
                        st.rerun()
                with col3:
                    if st.button("🗑️ Clear", use_container_width=True):
                        st.session_state.selected_layers = []
                        st.rerun()
                
                # Use session state for layer selection
                if 'selected_layers' in st.session_state:
                    selected_layers = st.session_state.selected_layers
                
                if selected_layers:
                    # Limit layers for performance
                    if len(selected_layers) > 3:
                        st.warning("⚠️ Only first 3 layers shown for performance")
                        selected_layers = selected_layers[:3]
                    
                    selected_indices = [layer_options.index(layer) for layer in selected_layers]
                    
                    # Create and display enhanced map
                    with st.spinner("🗺️ Creating enhanced interactive map..."):
                        try:
                            map_obj = analyzer.create_enhanced_geemap_visualization(
                                results['delta_images'], 
                                results['roi'],
                                selected_indices,
                                sensitivity_override,
                                vis_mode_override
                            )
                            
                            if map_obj:
                                # Display map using Streamlit
                                map_obj.to_streamlit(height=700)
                                
                                # Enhanced interpretation guide
                                with st.expander("🎯 Enhanced Map Interpretation Guide"):
                                    st.markdown(f"""
                                    **Current Settings:**
                                    - **Sensitivity**: {sensitivity_override.title()} (affects change detection threshold)
                                    - **Visualization Mode**: {vis_mode_override.title()} (adaptive = auto-scaling based on local data)
                                    
                                    **Color Interpretation:**
                                    - **Dark Blue**: Strong decrease in radar backscatter (major construction/excavation)
                                    - **Blue**: Moderate decrease (soil disturbance, vegetation removal)
                                    - **Light Blue**: Minor decrease (surface changes)
                                    - **White**: No significant change
                                    - **Pink**: Minor increase (small structures, surface hardening)
                                    - **Orange**: Moderate increase (building construction)
                                    - **Red**: Strong increase (new buildings, hardened surfaces)
                                    - **Dark Red**: Major increase (large new structures)
                                    
                                    **Red Boundary**: Study area ROI
                                    
                                    **Enhanced Features:**
                                    - **Adaptive Scaling**: Colors automatically adjust to local data range
                                    - **Speckle Filtering**: Reduced noise for clearer visualization
                                    - **Multi-temporal Analysis**: Compare changes across different periods
                                    - **Statistical Robustness**: Based on percentile analysis
                                    
                                    **Usage Tips:**
                                    - Use layer control panel to show/hide different months
                                    - Zoom in for detailed local analysis
                                    - Switch between sensitivity levels to focus on different change magnitudes
                                    - Compare adaptive vs standard modes for different perspectives
                                    """)
                                    
                                # Display current layer statistics
                                with st.expander("📊 Current Layer Statistics"):
                                    for idx in selected_indices:
                                        if idx < len(results['delta_images']):
                                            img_data = results['delta_images'][idx]
                                            if 'local_stats' in img_data and img_data['local_stats']:
                                                stats = img_data['local_stats']
                                                st.markdown(f"**{img_data['label']}:**")
                                                col1, col2, col3 = st.columns(3)
                                                with col1:
                                                    st.metric("5th Percentile", f"{stats.get('p5', 0):.4f}")
                                                    st.metric("25th Percentile", f"{stats.get('p25', 0):.4f}")
                                                with col2:
                                                    st.metric("Median", f"{stats.get('p50', 0):.4f}")
                                                    st.metric("75th Percentile", f"{stats.get('p75', 0):.4f}")
                                                with col3:
                                                    st.metric("95th Percentile", f"{stats.get('p95', 0):.4f}")
                                                    st.metric("Images Used", f"{img_data.get('image_count', 'N/A')}")
                            else:
                                st.error("❌ Failed to create enhanced map")
                        
                        except Exception as e:
                            st.error(f"❌ Enhanced map display error: {e}")
                            st.error(f"Full traceback: {traceback.format_exc()}")
                else:
                    st.info("👆 Please select at least one layer to display the enhanced map")
                
                # Enhanced Statistics table
                with st.expander("📋 Enhanced Detailed Statistics"):
                    df = pd.DataFrame(results['stats_data'])
                    
                    # Add formatted columns for better readability
                    if not df.empty:
                        df_display = df.copy()
                        df_display['mean_delta_formatted'] = df_display['mean_delta'].apply(lambda x: f"{x:.4f}")
                        df_display['std_delta_formatted'] = df_display['std_delta'].apply(lambda x: f"{x:.4f}")
                        df_display['range'] = df_display['max_delta'] - df_display['min_delta']
                        
                    st.dataframe(df_display, use_container_width=True)
                    
                    # Enhanced download functionality
                    col1, col2 = st.columns(2)
                    with col1:
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Enhanced Statistics as CSV",
                            data=csv,
                            file_name=f"enhanced_delta_vv_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Summary statistics
                        if not df.empty:
                            st.markdown("**Summary:**")
                            st.write(f"• Total months analyzed: {len(df)}")
                            st.write(f"• Average change: {df['mean_delta'].mean():.4f}")
                            st.write(f"• Max positive change: {df['mean_delta'].max():.4f}")
                            st.write(f"• Max negative change: {df['mean_delta'].min():.4f}")
            
            else:
                st.warning("⚠️ No data available for enhanced analysis. Please check your configuration and try again.")


    main()
if __name__ == "__main__":
=======
    # Enhanced Google Earth Engine Authentication Module
    # Service Account + Rectangle ROI + Delta VV Maps with Geemap - ENHANCED LOCAL VISUALIZATION

import streamlit as st
import geemap.foliumap as geemap
import ee
import json
import os
import tempfile
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from google.oauth2 import service_account
import traceback
from typing import Optional, Dict, Any, List
import numpy as np
import calendar

def run():
    st.title("🛰️ Monitoring de phase construction en utilisant la télédétection")





    class SimplifiedGEEAuth:
        """Simplified Google Earth Engine Authentication - Service Account Only"""
        
        def __init__(self):
            self.authenticated = False
            self.credentials = None
            
        def authenticate(self) -> bool:
            """Service Account authentication only"""
            st.subheader("🔐 Google Earth Engine Authentication")
            
            # Check if already authenticated
            if self.check_existing_auth():
                return True
            
            # Show service account upload interface
            return self.auth_with_file_upload()
        
        def check_existing_auth(self) -> bool:
            """Check if GEE is already authenticated"""
            try:
                test_result = ee.Number(1).getInfo()
                if test_result == 1:
                    st.success("✅ Google Earth Engine already authenticated!")
                    self.authenticated = True
                    return True
            except Exception:
                pass
            return False
        
        def auth_with_file_upload(self) -> bool:
            """Authentication via service account file upload"""
            
            st.markdown("### 📤 Upload Service Account JSON File")
            
            with st.expander("📋 How to get a Service Account file", expanded=False):
                st.markdown("""
                **Steps to create a Service Account:**
                1. Go to [Google Cloud Console](https://console.cloud.google.com/)
                2. Create or select a project
                3. Enable the Earth Engine API
                4. Go to IAM & Admin > Service Accounts
                5. Create a new service account
                6. Download the JSON key file
                7. Upload it below
                """)
            
            uploaded_file = st.file_uploader(
                "Select your service account JSON file:",
                type=['json'],
                help="Upload the service account key file downloaded from Google Cloud Console"
            )
            
            if uploaded_file is not None:
                if st.button("🔐 Authenticate", key="auth_button"):
                    return self.process_uploaded_file(uploaded_file)
            
            return False
        
        def process_uploaded_file(self, uploaded_file) -> bool:
            """Process the uploaded service account file"""
            try:
                file_content = uploaded_file.read()
                uploaded_file.seek(0)
                
                try:
                    credentials_dict = json.loads(file_content)
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON file: {str(e)}")
                    return False
                
                # Validate service account structure
                required_fields = ['type', 'project_id', 'private_key', 'client_email']
                missing_fields = [field for field in required_fields if field not in credentials_dict]
                
                if missing_fields:
                    st.error(f"❌ Missing required fields: {', '.join(missing_fields)}")
                    return False
                
                if credentials_dict.get('type') != 'service_account':
                    st.error("❌ File is not a valid service account")
                    return False
                
                # Create temporary file for authentication
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                    json.dump(credentials_dict, temp_file, indent=2)
                    temp_file_path = temp_file.name
                
                try:
                    credentials = service_account.Credentials.from_service_account_file(
                        temp_file_path,
                        scopes=['https://www.googleapis.com/auth/earthengine']
                    )
                    
                    ee.Initialize(credentials)
                    
                    # Test authentication
                    test_result = ee.Number(42).getInfo()
                    
                    if test_result == 42:
                        st.success("✅ Authentication successful!")
                        st.success(f"🎯 Project: {credentials_dict.get('project_id', 'Unknown')}")
                        st.success(f"📧 Service Account: {credentials_dict.get('client_email', 'Unknown')}")
                        
                        self.authenticated = True
                        self.credentials = credentials
                        
                        # Store in session state
                        st.session_state.gee_credentials = credentials_dict
                        st.session_state.gee_authenticated = True
                        
                        return True
                    else:
                        st.error("❌ Authentication test failed")
                        return False
                        
                except Exception as e:
                    st.error(f"❌ Authentication failed: {str(e)}")
                    return False
                
                finally:
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
            
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                return False
        
        def is_authenticated(self) -> bool:
            """Check if currently authenticated"""
            if not self.authenticated:
                return False
            
            try:
                ee.Number(1).getInfo()
                return True
            except:
                self.authenticated = False
                return False


    class GEEGeomapAnalyzer:
        """GEE Analyzer using Geemap for Delta VV visualization - ENHANCED LOCAL CHANGES"""
        
        def __init__(self):
            self.auth_manager = SimplifiedGEEAuth()
            # Enhanced palettes for better local visualization
            self.palette_fine = ['#000080', '#0000FF', '#4169E1', '#87CEEB', '#FFFFFF', '#FFB6C1', '#FF4500', '#FF0000', '#8B0000']
            self.palette_coarse = ['#0000FF', '#FFFFFF', '#FF0000']
            
            # Multiple visualization parameter sets
            self.vis_params_adaptive = {'min': -0.02, 'max': 0.02, 'palette': self.palette_fine}
            self.vis_params_sensitive = {'min': -0.01, 'max': 0.01, 'palette': self.palette_fine}
            self.vis_params_robust = {'min': -0.05, 'max': 0.05, 'palette': self.palette_fine}
            
        def ensure_authentication(self) -> bool:
            """Ensure GEE is authenticated"""
            if self.auth_manager.is_authenticated():
                return True
            
            st.warning("⚠️ Google Earth Engine authentication required")
            return self.auth_manager.authenticate()
            
        def preprocess_s1(self, img, roi):
            """Enhanced Sentinel-1 preprocessing with noise reduction - FIXED VERSION"""
            try:
                # Get VV band
                vv = img.select('VV')
                
                # Convert to dB and scale
                vv_db = vv.multiply(0.0001)
                
                # Apply speckle filtering using focal_mean with radius parameter
                # Use a numeric radius instead of kernel for focal_mean
                vv_filtered = vv_db.focal_mean(radius=1.5, kernelType='square', units='pixels')
                
                # Alternative approach using convolve if you prefer kernel-based filtering:
                # kernel = ee.Kernel.square(1.5, 'pixels', False)
                # vv_filtered = vv_db.convolve(kernel.normalize())
                
                # Clip to ROI
                vv_clipped = vv_filtered.clip(roi)
                
                return vv_clipped.copyProperties(img, ["system:time_start"])
                
            except Exception as e:
                st.error(f"❌ Error preprocessing Sentinel-1: {e}")
                return None
        
        def get_monthly_delta_enhanced(self, year: int, month: int, reference_img, roi):
            """Enhanced monthly delta calculation with better statistics"""
            try:
                # Create start and end dates for the month
                start = ee.Date(f"{year}-{month:02d}-01")
                end = start.advance(1, 'month')
                
                # Get monthly collection with more strict filtering
                monthly_collection = ee.ImageCollection("COPERNICUS/S1_GRD") \
                    .filterBounds(roi) \
                    .filterDate(start, end) \
                    .filter(ee.Filter.eq('instrumentMode', 'IW')) \
                    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
                    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))  # Use only descending passes for consistency
                
                # Check if we have data
                size = monthly_collection.size().getInfo()
                if size == 0:
                    return None, None
                
                # Process images and get median
                processed_collection = monthly_collection.map(lambda img: self.preprocess_s1(img, roi))
                monthly_median = processed_collection.median()
                
                # Calculate delta
                delta = monthly_median.subtract(reference_img).rename(f'delta_VV_{year}_{month:02d}')
                
                # Calculate local statistics for adaptive visualization
                local_stats = delta.reduceRegion(
                    reducer=ee.Reducer.percentile([5, 25, 50, 75, 95]),
                    geometry=roi,
                    scale=10,
                    maxPixels=1e9
                ).getInfo()
                
                delta_with_props = delta.set({
                    'year': year, 
                    'month': month,
                    'image_count': size,
                    'p5': local_stats.get(f'delta_VV_{year}_{month:02d}_p5', -0.02),
                    'p25': local_stats.get(f'delta_VV_{year}_{month:02d}_p25', -0.01),
                    'p50': local_stats.get(f'delta_VV_{year}_{month:02d}_p50', 0),
                    'p75': local_stats.get(f'delta_VV_{year}_{month:02d}_p75', 0.01),
                    'p95': local_stats.get(f'delta_VV_{year}_{month:02d}_p95', 0.02)
                })
                
                return delta_with_props, local_stats
                
            except Exception as e:
                st.warning(f"⚠️ Error calculating monthly delta for {year}-{month:02d}: {e}")
                return None, None
        
        def create_reference_image_enhanced(self, roi, ref_start: str, ref_end: str):
            """Enhanced reference image creation"""
            try:
                st.info(f"🔍 Creating enhanced reference image for period: {ref_start} to {ref_end}")
                
                ref_collection = ee.ImageCollection("COPERNICUS/S1_GRD") \
                    .filterBounds(roi) \
                    .filterDate(ref_start, ref_end) \
                    .filter(ee.Filter.eq('instrumentMode', 'IW')) \
                    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
                    .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
                
                size = ref_collection.size().getInfo()
                if size == 0:
                    st.error(f"❌ No Sentinel-1 images found for reference period")
                    return None
                
                st.success(f"✅ Found {size} images for reference period")
                
                # Process reference images with enhanced filtering
                processed_ref = ref_collection.map(lambda img: self.preprocess_s1(img, roi))
                reference_img = processed_ref.median()
                
                return reference_img
                
            except Exception as e:
                st.error(f"❌ Error creating reference image: {e}")
                return None
        
        def create_rectangle_roi(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float):
            """Create rectangular ROI from coordinates"""
            try:
                roi = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])
                st.success(f"✅ Rectangle ROI created: ({lat_min}, {lon_min}) to ({lat_max}, {lon_max})")
                return roi
            except Exception as e:
                st.error(f"❌ Error creating rectangle ROI: {e}")
                return None
        
        def get_adaptive_vis_params(self, local_stats: Dict, sensitivity: str = "medium"):
            """Get adaptive visualization parameters based on local statistics"""
            try:
                if not local_stats:
                    return self.vis_params_adaptive
                
                # Extract percentiles
                p5 = local_stats.get('p5', -0.02)
                p95 = local_stats.get('p95', 0.02)
                p25 = local_stats.get('p25', -0.01)
                p75 = local_stats.get('p75', 0.01)
                
                if sensitivity == "high":
                    # Use 25th-75th percentiles for high sensitivity
                    min_val = max(p25, -0.03)
                    max_val = min(p75, 0.03)
                elif sensitivity == "low":
                    # Use 5th-95th percentiles for low sensitivity
                    min_val = max(p5, -0.05)
                    max_val = min(p95, 0.05)
                else:  # medium
                    # Use adaptive range
                    range_val = max(abs(p5), abs(p95))
                    min_val = max(-range_val, -0.04)
                    max_val = min(range_val, 0.04)
                
                return {
                    'min': min_val,
                    'max': max_val,
                    'palette': self.palette_fine
                }
                
            except Exception as e:
                st.warning(f"⚠️ Error calculating adaptive parameters: {e}")
                return self.vis_params_adaptive
        
        def analyze_delta_vv_enhanced(self, lat_min: float, lat_max: float, 
                                    lon_min: float, lon_max: float,
                                    start_year: int, end_year: int,
                                    start_month: int, end_month: int,
                                    ref_start: str, ref_end: str):
            """Enhanced main analysis function"""
            if not self.ensure_authentication():
                return [], [], None
            
            try:
                st.info("🛰️ Starting Enhanced Delta VV analysis...")
                
                # Create ROI
                roi = self.create_rectangle_roi(lat_min, lat_max, lon_min, lon_max)
                if roi is None:
                    return [], [], None
                
                # Create enhanced reference image
                reference_img = self.create_reference_image_enhanced(roi, ref_start, ref_end)
                if reference_img is None:
                    return [], [], None
                
                # Calculate Delta VV images with enhanced processing
                delta_images = []
                stats_data = []
                
                total_months = 0
                for year in range(start_year, end_year + 1):
                    for month in range(1, 13):
                        if year == start_year and month < start_month:
                            continue
                        if year == end_year and month > end_month:
                            break
                        total_months += 1
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                current_month = 0
                
                for year in range(start_year, end_year + 1):
                    for month in range(1, 13):
                        if year == start_year and month < start_month:
                            continue
                        if year == end_year and month > end_month:
                            break
                        
                        current_month += 1
                        progress = current_month / total_months
                        progress_bar.progress(progress)
                        status_text.text(f"Processing {calendar.month_abbr[month]} {year} ({current_month}/{total_months})")
                        
                        try:
                            delta_img, local_stats = self.get_monthly_delta_enhanced(year, month, reference_img, roi)
                            
                            if delta_img is not None and local_stats is not None:
                                # Calculate comprehensive statistics
                                stats = delta_img.reduceRegion(
                                    reducer=ee.Reducer.mean().combine(
                                        ee.Reducer.stdDev(), sharedInputs=True
                                    ).combine(
                                        ee.Reducer.minMax(), sharedInputs=True
                                    ).combine(
                                        ee.Reducer.percentile([10, 25, 50, 75, 90]), sharedInputs=True
                                    ),
                                    geometry=roi,
                                    scale=10,
                                    maxPixels=1e9
                                ).getInfo()
                                
                                if stats:
                                    delta_key = f'delta_VV_{year}_{month:02d}'
                                    stats_data.append({
                                        'date': f'{year}-{month:02d}-01',
                                        'year': year,
                                        'month': month,
                                        'month_name': calendar.month_abbr[month],
                                        'mean_delta': stats.get(f'{delta_key}_mean', 0),
                                        'std_delta': stats.get(f'{delta_key}_stdDev', 0),
                                        'min_delta': stats.get(f'{delta_key}_min', 0),
                                        'max_delta': stats.get(f'{delta_key}_max', 0),
                                        'p10': stats.get(f'{delta_key}_p10', 0),
                                        'p25': stats.get(f'{delta_key}_p25', 0),
                                        'p50': stats.get(f'{delta_key}_p50', 0),
                                        'p75': stats.get(f'{delta_key}_p75', 0),
                                        'p90': stats.get(f'{delta_key}_p90', 0),
                                        'image_count': delta_img.get('image_count').getInfo()
                                    })
                                    
                                    # Get adaptive visualization parameters
                                    adaptive_vis = self.get_adaptive_vis_params(local_stats, "medium")
                                    
                                    delta_images.append({
                                        'image': delta_img,
                                        'date': f'{calendar.month_abbr[month]} {year}',
                                        'year': year,
                                        'month': month,
                                        'label': f'ΔVV {calendar.month_abbr[month]} {year}',
                                        'local_stats': local_stats,
                                        'adaptive_vis': adaptive_vis
                                    })
                        
                        except Exception as e:
                            st.warning(f"⚠️ Error processing {calendar.month_abbr[month]} {year}: {e}")
                
                progress_bar.progress(1.0)
                status_text.text(f"✅ Enhanced analysis complete! Processed {len(stats_data)} months")
                
                return delta_images, stats_data, roi
                
            except Exception as e:
                st.error(f"❌ Error in enhanced analysis: {e}")
                return [], [], None
        
        def create_enhanced_geemap_visualization(self, delta_images: List, roi, selected_indices: List[int] = None, 
                                            sensitivity: str = "medium", vis_mode: str = "adaptive"):
            """Enhanced Geemap visualization with multiple visualization modes - ROI BOUNDARY REMOVED"""
            try:
                if not delta_images:
                    st.warning("⚠️ No delta images available for mapping")
                    return None
                
                # Get ROI coordinates for centering
                try:
                    roi_coords = roi.coordinates().getInfo()
                    if roi_coords and len(roi_coords) > 0 and len(roi_coords[0]) > 0:
                        coords = roi_coords[0]
                        center_lat = (coords[0][1] + coords[2][1]) / 2
                        center_lon = (coords[0][0] + coords[2][0]) / 2
                    else:
                        center_lat, center_lon = 33.575, -7.5875
                except Exception:
                    center_lat, center_lon = 33.575, -7.5875
                
                # Create Enhanced Geemap Map
                Map = geemap.Map(
                    center=[center_lat, center_lon],
                    zoom=15,  # Higher zoom for local details
                    height=700
                )
                
                # Add high-resolution satellite basemap
                Map.add_basemap('SATELLITE')
                
                # ROI BOUNDARY SECTION COMMENTED OUT - NO MORE RED RECTANGLE!
                # try:
                #     roi_feature = ee.Feature(roi, {'name': 'Study Area'})
                #     roi_collection = ee.FeatureCollection([roi_feature])
                #     
                #     Map.addLayer(roi_collection, {
                #         'color': '#FF0000',
                #         'width': 3,
                #         'fillColor': '00000000'  # Transparent fill
                #     }, "ROI Boundary", True, 1.0)
                #     
                #     st.success("✅ ROI boundary added")
                #     
                # except Exception as roi_error:
                #     st.warning(f"⚠️ Could not add ROI boundary: {roi_error}")
                
                # Add selected delta layers with enhanced visualization
                if selected_indices is None:
                    selected_indices = list(range(min(2, len(delta_images))))
                
                st.info(f"Adding {len(selected_indices)} enhanced delta VV layers...")
                
                added_layers = 0
                for i, idx in enumerate(selected_indices):
                    if idx < len(delta_images):
                        delta_data = delta_images[idx]
                        delta_img = delta_data['image']
                        label = delta_data['label']
                        
                        # Choose visualization parameters based on mode
                        if vis_mode == "adaptive" and 'adaptive_vis' in delta_data:
                            vis_params = delta_data['adaptive_vis']
                        elif vis_mode == "sensitive":
                            vis_params = self.vis_params_sensitive
                        elif vis_mode == "robust":
                            vis_params = self.vis_params_robust
                        else:  # standard
                            vis_params = self.vis_params_adaptive
                        
                        # Adjust sensitivity
                        if sensitivity == "high":
                            vis_params['min'] = vis_params['min'] * 0.5
                            vis_params['max'] = vis_params['max'] * 0.5
                        elif sensitivity == "low":
                            vis_params['min'] = vis_params['min'] * 2
                            vis_params['max'] = vis_params['max'] * 2
                        
                        try:
                            Map.addLayer(
                                delta_img,
                                vis_params,
                                f"{label} ({vis_mode})",
                                True,
                                0.8
                            )
                            added_layers += 1
                            st.success(f"✅ Added: {label} (range: {vis_params['min']:.3f} to {vis_params['max']:.3f})")
                            
                        except Exception as layer_error:
                            st.error(f"❌ Failed to add {label}: {str(layer_error)}")
                            continue
                
                if added_layers == 0:
                    st.error("❌ No layers were successfully added")
                    return None
                
                # Add layer control
                Map.add_layer_control()
                
                # Add enhanced legend
                legend_dict = {
                    'Major Decrease (Construction)': '#000080',
                    'Moderate Decrease': '#0000FF', 
                    'Light Decrease': '#4169E1',
                    'Minimal Change': '#87CEEB',
                    'No Change': '#FFFFFF',
                    'Minimal Increase': '#FFB6C1',
                    'Light Increase': '#FF4500',
                    'Moderate Increase': '#FF0000',
                    'Major Increase (New Structures)': '#8B0000'
                }
                
                try:
                    Map.add_legend(legend_dict=legend_dict, title=f"Delta VV Changes ({vis_mode} mode)")
                except Exception:
                    pass
                
                st.success(f"✅ Enhanced map created with {added_layers} layers in {vis_mode} mode (ROI boundary hidden)")
                return Map
                
            except Exception as e:
                st.error(f"❌ Error creating enhanced map: {e}")
                return None
        
        def create_enhanced_time_series_plot(self, stats_data: List[Dict]):
            """Enhanced time series plot with percentiles"""
            try:
                df = pd.DataFrame(stats_data)
                
                fig = go.Figure()
                
                # Main time series
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['mean_delta'],
                    mode='lines+markers',
                    name='Mean Delta VV',
                    line=dict(color='blue', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>%{x}</b><br>Mean ΔVV: %{y:.4f}<extra></extra>'
                ))
                
                # Add percentile bands
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['p75'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['p25'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(0,100,80,0.2)',
                    name='25th-75th Percentile',
                    hoverinfo='skip'
                ))
                
                # Add median line
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['p50'],
                    mode='lines',
                    name='Median Delta VV',
                    line=dict(color='green', width=2, dash='dash'),
                    hovertemplate='<b>%{x}</b><br>Median ΔVV: %{y:.4f}<extra></extra>'
                ))
                
                fig.update_layout(
                    title='📈 Enhanced Evolution of Radar Backscatter Changes (Delta VV)',
                    xaxis_title='Date',
                    yaxis_title='Delta VV (dB)',
                    hovermode='x unified',
                    showlegend=True,
                    height=600
                )
                
                return fig
                
            except Exception as e:
                st.error(f"❌ Error creating enhanced plot: {e}")
                return None


    def create_enhanced_configuration_interface():
        """Enhanced configuration interface"""
        st.subheader("📍 Enhanced Study Area Configuration")
        
        # ROI Configuration
        st.markdown("#### Rectangle ROI Definition")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Southwest Corner (Bottom-left)**")
            lat_min = st.number_input("Latitude Min", value=33.5700, format="%.6f", key="lat_min")
            lon_min = st.number_input("Longitude Min", value=-7.5950, format="%.6f", key="lon_min")
        
        with col2:
            st.markdown("**Northeast Corner (Top-right)**")
            lat_max = st.number_input("Latitude Max", value=33.5800, format="%.6f", key="lat_max")
            lon_max = st.number_input("Longitude Max", value=-7.5800, format="%.6f", key="lon_max")
        
        # Validation
        if lat_min >= lat_max:
            st.error("❌ Latitude Min must be less than Latitude Max")
        if lon_min >= lon_max:
            st.error("❌ Longitude Min must be less than Longitude Max")
        
        # Calculate area
        lat_diff = lat_max - lat_min
        lon_diff = lon_max - lon_min
        area_km2 = lat_diff * lon_diff * 111 * 111 * np.cos(np.radians((lat_min + lat_max)/2))
        st.info(f"📏 Approximate area: {area_km2:.2f} km²")
        
        # Time Period Configuration
        st.markdown("#### Analysis Period")
        col1, col2 = st.columns(2)
        
        with col1:
            start_year = st.number_input("Start Year", value=2024, min_value=2020, max_value=2025)
            start_month = st.selectbox("Start Month", options=list(range(1, 13)), 
                                    format_func=lambda x: calendar.month_name[x], index=4)
        
        with col2:
            end_year = st.number_input("End Year", value=2025, min_value=2020, max_value=2025)
            end_month = st.selectbox("End Month", options=list(range(1, 13)), 
                                format_func=lambda x: calendar.month_name[x], index=5)
        
        # Reference Period
        st.markdown("#### Reference Period")
        st.info("Period before construction work for comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            ref_start = st.date_input("Reference Start", value=datetime(2024, 4, 1))
        with col2:
            ref_end = st.date_input("Reference End", value=datetime(2024, 5, 1))
        
        # Enhanced Visualization Options
        st.markdown("#### 🎨 Enhanced Visualization Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sensitivity = st.selectbox(
                "Sensitivity Level",
                options=["high", "medium", "low"],
                index=1,
                help="High: More sensitive to small changes, Low: Focus on larger changes"
            )
        
        with col2:
            vis_mode = st.selectbox(
                "Visualization Mode",
                options=["adaptive", "sensitive", "standard", "robust"],
                index=0,
                help="Adaptive: Auto-adjust based on data, Sensitive: Fixed high sensitivity"
            )
        
        with col3:
            filter_mode = st.selectbox(
                "Image Filtering",
                options=["enhanced", "standard"],
                index=0,
                help="Enhanced: Apply speckle filtering, Standard: Basic processing"
            )
        
        return (lat_min, lat_max, lon_min, lon_max, 
                start_year, end_year, start_month, end_month,
                ref_start.strftime('%Y-%m-%d'), ref_end.strftime('%Y-%m-%d'),
                sensitivity, vis_mode, filter_mode)



    def main():
        """Enhanced Main application - FIXED VERSION"""
        
        # Initialize analyzer
        if 'gee_analyzer' not in st.session_state:
            st.session_state.gee_analyzer = GEEGeomapAnalyzer()
        
        analyzer = st.session_state.gee_analyzer
        
        st.markdown("*Enhanced Delta VV Analysis and Visualization - ENHANCED LOCAL VISUALIZATION*")
        
        # Authentication section
        st.subheader("🔐 Authentication")
        
        if analyzer.auth_manager.is_authenticated():
            st.success("✅ Google Earth Engine authenticated!")
            
            if st.button("🔄 Re-authenticate"):
                analyzer.auth_manager.authenticated = False
                st.rerun()
        else:
            if not analyzer.ensure_authentication():
                st.stop()
        
        # Enhanced Configuration
        (lat_min, lat_max, lon_min, lon_max, 
        start_year, end_year, start_month, end_month,
        ref_start, ref_end, sensitivity, vis_mode, filter_mode) = create_enhanced_configuration_interface()

        # Validation before analysis
        if lat_min >= lat_max or lon_min >= lon_max:
            st.error("❌ Please correct the coordinate bounds before proceeding")
            st.stop()
        
        # Enhanced Analysis button
        if st.button("🚀 Launch Enhanced Delta VV Analysis", type="primary", use_container_width=True):
            with st.spinner("🛰️ Analyzing satellite data with enhanced processing..."):
                delta_images, stats_data, roi = analyzer.analyze_delta_vv_enhanced(
                    lat_min, lat_max, lon_min, lon_max,
                    start_year, end_year, start_month, end_month,
                    ref_start, ref_end
                )
                
                # Store results with enhanced config
                st.session_state.analysis_results = {
                    'delta_images': delta_images,
                    'stats_data': stats_data,
                    'roi': roi,
                    'config': {
                        'lat_min': lat_min, 'lat_max': lat_max,
                        'lon_min': lon_min, 'lon_max': lon_max,
                        'start_year': start_year, 'end_year': end_year,
                        'start_month': start_month, 'end_month': end_month,
                        'sensitivity': sensitivity,
                        'vis_mode': vis_mode,
                        'filter_mode': filter_mode
                    }
                }
                
                st.success("✅ Enhanced analysis completed!")
        
        # Enhanced Results section
        if 'analysis_results' in st.session_state:
            results = st.session_state.analysis_results
            
            if results['stats_data'] and results['delta_images']:
                st.subheader("📊 Enhanced Analysis Results")
                
                # Enhanced Time series plot
                st.markdown("### 📈 Enhanced Time Series Analysis")
                fig = analyzer.create_enhanced_time_series_plot(results['stats_data'])
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Enhanced Geemap visualization
                st.markdown("### 🗺️ Enhanced Interactive Delta VV Maps")
                st.info("💡 Enhanced visualization shows changes in radar backscatter with adaptive scaling. Blue = decrease (construction/disturbance), Red = increase (new structures)")
                
                # Enhanced Layer selection with visualization controls
                layer_options = [f"{img['label']}" for img in results['delta_images']]
                
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    selected_layers = st.multiselect(
                        "Select layers to display:",
                        options=layer_options,
                        default=layer_options[-2:] if len(layer_options) >= 2 else layer_options,
                        help="Select which months to display (max 3 for performance)"
                    )
                
                with col2:
                    # Get sensitivity and vis_mode from stored config or use defaults
                    current_sensitivity = results['config'].get('sensitivity', 'medium')
                    current_vis_mode = results['config'].get('vis_mode', 'adaptive')
                    
                    sensitivity_override = st.selectbox(
                        "Sensitivity:",
                        options=["high", "medium", "low"],
                        index=["high", "medium", "low"].index(current_sensitivity),
                        help="Override sensitivity for visualization"
                    )
                
                with col3:
                    vis_mode_override = st.selectbox(
                        "Viz Mode:",
                        options=["adaptive", "sensitive", "standard", "robust"],
                        index=["adaptive", "sensitive", "standard", "robust"].index(current_vis_mode),
                        help="Override visualization mode"
                    )
                
                # Quick selection buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔄 Latest 2", use_container_width=True):
                        st.session_state.selected_layers = layer_options[-2:] if len(layer_options) >= 2 else layer_options
                        st.rerun()
                with col2:
                    if st.button("📊 All Data", use_container_width=True):
                        st.session_state.selected_layers = layer_options
                        st.rerun()
                with col3:
                    if st.button("🗑️ Clear", use_container_width=True):
                        st.session_state.selected_layers = []
                        st.rerun()
                
                # Use session state for layer selection
                if 'selected_layers' in st.session_state:
                    selected_layers = st.session_state.selected_layers
                
                if selected_layers:
                    # Limit layers for performance
                    if len(selected_layers) > 3:
                        st.warning("⚠️ Only first 3 layers shown for performance")
                        selected_layers = selected_layers[:3]
                    
                    selected_indices = [layer_options.index(layer) for layer in selected_layers]
                    
                    # Create and display enhanced map
                    with st.spinner("🗺️ Creating enhanced interactive map..."):
                        try:
                            map_obj = analyzer.create_enhanced_geemap_visualization(
                                results['delta_images'], 
                                results['roi'],
                                selected_indices,
                                sensitivity_override,
                                vis_mode_override
                            )
                            
                            if map_obj:
                                # Display map using Streamlit
                                map_obj.to_streamlit(height=700)
                                
                                # Enhanced interpretation guide
                                with st.expander("🎯 Enhanced Map Interpretation Guide"):
                                    st.markdown(f"""
                                    **Current Settings:**
                                    - **Sensitivity**: {sensitivity_override.title()} (affects change detection threshold)
                                    - **Visualization Mode**: {vis_mode_override.title()} (adaptive = auto-scaling based on local data)
                                    
                                    **Color Interpretation:**
                                    - **Dark Blue**: Strong decrease in radar backscatter (major construction/excavation)
                                    - **Blue**: Moderate decrease (soil disturbance, vegetation removal)
                                    - **Light Blue**: Minor decrease (surface changes)
                                    - **White**: No significant change
                                    - **Pink**: Minor increase (small structures, surface hardening)
                                    - **Orange**: Moderate increase (building construction)
                                    - **Red**: Strong increase (new buildings, hardened surfaces)
                                    - **Dark Red**: Major increase (large new structures)
                                    
                                    **Red Boundary**: Study area ROI
                                    
                                    **Enhanced Features:**
                                    - **Adaptive Scaling**: Colors automatically adjust to local data range
                                    - **Speckle Filtering**: Reduced noise for clearer visualization
                                    - **Multi-temporal Analysis**: Compare changes across different periods
                                    - **Statistical Robustness**: Based on percentile analysis
                                    
                                    **Usage Tips:**
                                    - Use layer control panel to show/hide different months
                                    - Zoom in for detailed local analysis
                                    - Switch between sensitivity levels to focus on different change magnitudes
                                    - Compare adaptive vs standard modes for different perspectives
                                    """)
                                    
                                # Display current layer statistics
                                with st.expander("📊 Current Layer Statistics"):
                                    for idx in selected_indices:
                                        if idx < len(results['delta_images']):
                                            img_data = results['delta_images'][idx]
                                            if 'local_stats' in img_data and img_data['local_stats']:
                                                stats = img_data['local_stats']
                                                st.markdown(f"**{img_data['label']}:**")
                                                col1, col2, col3 = st.columns(3)
                                                with col1:
                                                    st.metric("5th Percentile", f"{stats.get('p5', 0):.4f}")
                                                    st.metric("25th Percentile", f"{stats.get('p25', 0):.4f}")
                                                with col2:
                                                    st.metric("Median", f"{stats.get('p50', 0):.4f}")
                                                    st.metric("75th Percentile", f"{stats.get('p75', 0):.4f}")
                                                with col3:
                                                    st.metric("95th Percentile", f"{stats.get('p95', 0):.4f}")
                                                    st.metric("Images Used", f"{img_data.get('image_count', 'N/A')}")
                            else:
                                st.error("❌ Failed to create enhanced map")
                        
                        except Exception as e:
                            st.error(f"❌ Enhanced map display error: {e}")
                            st.error(f"Full traceback: {traceback.format_exc()}")
                else:
                    st.info("👆 Please select at least one layer to display the enhanced map")
                
                # Enhanced Statistics table
                with st.expander("📋 Enhanced Detailed Statistics"):
                    df = pd.DataFrame(results['stats_data'])
                    
                    # Add formatted columns for better readability
                    if not df.empty:
                        df_display = df.copy()
                        df_display['mean_delta_formatted'] = df_display['mean_delta'].apply(lambda x: f"{x:.4f}")
                        df_display['std_delta_formatted'] = df_display['std_delta'].apply(lambda x: f"{x:.4f}")
                        df_display['range'] = df_display['max_delta'] - df_display['min_delta']
                        
                    st.dataframe(df_display, use_container_width=True)
                    
                    # Enhanced download functionality
                    col1, col2 = st.columns(2)
                    with col1:
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Enhanced Statistics as CSV",
                            data=csv,
                            file_name=f"enhanced_delta_vv_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Summary statistics
                        if not df.empty:
                            st.markdown("**Summary:**")
                            st.write(f"• Total months analyzed: {len(df)}")
                            st.write(f"• Average change: {df['mean_delta'].mean():.4f}")
                            st.write(f"• Max positive change: {df['mean_delta'].max():.4f}")
                            st.write(f"• Max negative change: {df['mean_delta'].min():.4f}")
            
            else:
                st.warning("⚠️ No data available for enhanced analysis. Please check your configuration and try again.")


    main()
if __name__ == "__main__":
>>>>>>> 9ba0955f04e86c2f7e986ab511406cd53ae3e8d1
    run()