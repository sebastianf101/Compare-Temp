import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import zipfile
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Create output directory if it doesn't exist
        os.makedirs('plots', exist_ok=True)
        logger.info("Created plots directory")

        # Check if the zip file exists
        if not os.path.exists('smn_historical_data.zip'):
            raise FileNotFoundError("smn_historical_data.zip not found")

        # Read the data from the zip file
        logger.info("Reading data from zip file")
        with zipfile.ZipFile('smn_historical_data.zip', 'r') as zip_ref:
            # Get the CSV file name from the zip
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
            if not csv_files:
                raise ValueError("No CSV file found in the zip archive")
            
            csv_file = csv_files[0]
            logger.info(f"Found CSV file: {csv_file}")
            
            with zip_ref.open(csv_file) as f:
                df = pd.read_csv(f)
                logger.info(f"Successfully read {len(df)} rows of data")

        # Convert date strings to datetime and extract month
        logger.info("Processing dates")
        df['date'] = pd.to_datetime(df['date'].astype(str).str.zfill(8), format='%d%m%Y')
        df['month'] = df['date'].dt.month

        # Get the date range for the title
        start_date = df['date'].min().strftime('%Y')
        end_date = df['date'].max().strftime('%Y')
        date_range = f"{start_date}-{end_date}" if start_date != end_date else start_date
        logger.info(f"Data range: {date_range}")

        # Define seasons for Southern Hemisphere
        season_map = {
            12: 'Summer', 1: 'Summer', 2: 'Summer',
            3: 'Autumn', 4: 'Autumn', 5: 'Autumn',
            6: 'Winter', 7: 'Winter', 8: 'Winter',
            9: 'Spring', 10: 'Spring', 11: 'Spring'
        }
        df['season'] = df['month'].map(season_map)

        # Filter for the two stations
        stations = ['BUENOS AIRES OBSERVATORIO', 'TANDIL AERO']
        df_filtered = df[df['station'].isin(stations)]
        logger.info(f"Filtered data for stations: {stations}")

        # Calculate statistics by hour and season for each station
        logger.info("Calculating statistics")
        seasonal_hourly_stats = df_filtered.groupby(['season', 'station', 'hour'])['temperature'].agg([
            'mean', 'median', 'max', 'min', 'std'
        ]).unstack(level=1)

        # Set up the color scheme and line styles
        colors = {
            'BUENOS AIRES OBSERVATORIO': '#1f77b4',  # Blue
            'TANDIL AERO': '#ff7f0e',  # Orange
            'temp_diff': '#d62728'  # Red
        }

        line_styles = {
            'mean': '-',
            'median': '--',
            'max': ':',
            'min': ':'
        }

        # Create a figure for all seasons
        logger.info("Creating combined plot")
        plt.figure(figsize=(15, 10))
        sns.set_style("whitegrid")
        sns.set_palette("husl")

        # Plot each season in a subplot
        for i, season in enumerate(['Summer', 'Autumn', 'Winter', 'Spring'], 1):
            plt.subplot(2, 2, i)
            
            season_data = seasonal_hourly_stats.loc[season]
            
            # Calculate temperature differences
            season_data[('mean_diff', '')] = season_data[('mean', 'BUENOS AIRES OBSERVATORIO')] - season_data[('mean', 'TANDIL AERO')]
            season_data[('median_diff', '')] = season_data[('median', 'BUENOS AIRES OBSERVATORIO')] - season_data[('median', 'TANDIL AERO')]
            
            # Plot statistics for Buenos Aires
            for stat in ['mean', 'median', 'max', 'min']:
                plt.plot(season_data.index, season_data[(stat, 'BUENOS AIRES OBSERVATORIO')],
                         label=f'BA {stat.capitalize()}', color=colors['BUENOS AIRES OBSERVATORIO'],
                         linestyle=line_styles[stat], alpha=0.7)
            
            # Plot statistics for Tandil
            for stat in ['mean', 'median', 'max', 'min']:
                plt.plot(season_data.index, season_data[(stat, 'TANDIL AERO')],
                         label=f'Tandil {stat.capitalize()}', color=colors['TANDIL AERO'],
                         linestyle=line_styles[stat], alpha=0.7)
            
            # Plot temperature differences
            plt.plot(season_data.index, season_data[('mean_diff', '')],
                     label='Mean Difference', color=colors['temp_diff'],
                     linestyle='-', alpha=0.7)
            plt.plot(season_data.index, season_data[('median_diff', '')],
                     label='Median Difference', color=colors['temp_diff'],
                     linestyle='--', alpha=0.7)
            
            # Add statistics to the plot
            avg_diff = season_data[('mean_diff', '')].mean()
            max_diff = season_data[('mean_diff', '')].max()
            min_diff = season_data[('mean_diff', '')].min()
            
            stats_text = f'Avg Diff: {avg_diff:.1f}°C\nMax Diff: {max_diff:.1f}°C\nMin Diff: {min_diff:.1f}°C'
            plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.title(f'{season} Temperature Comparison')
            plt.xlabel('Hour of Day')
            plt.ylabel('Temperature (°C)')
            plt.xticks(range(0, 24, 2))
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)

        # Add overall title and adjust layout
        plt.suptitle(f'Temperature Comparison: Buenos Aires vs Tandil ({date_range})', fontsize=16, y=1.02)
        plt.tight_layout()
        output_file = 'plots/temperature_comparison_all_seasons.png'
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        plt.close()
        logger.info(f"Saved combined plot to {output_file}")

        # Create individual plots for each season
        for season in ['Summer', 'Autumn', 'Winter', 'Spring']:
            logger.info(f"Creating plot for {season}")
            plt.figure(figsize=(12, 6))
            sns.set_style("whitegrid")
            
            season_data = seasonal_hourly_stats.loc[season]
            
            # Calculate temperature differences
            season_data[('mean_diff', '')] = season_data[('mean', 'BUENOS AIRES OBSERVATORIO')] - season_data[('mean', 'TANDIL AERO')]
            season_data[('median_diff', '')] = season_data[('median', 'BUENOS AIRES OBSERVATORIO')] - season_data[('median', 'TANDIL AERO')]
            
            # Plot statistics for Buenos Aires
            for stat in ['mean', 'median', 'max', 'min']:
                plt.plot(season_data.index, season_data[(stat, 'BUENOS AIRES OBSERVATORIO')],
                         label=f'BA {stat.capitalize()}', color=colors['BUENOS AIRES OBSERVATORIO'],
                         linestyle=line_styles[stat], alpha=0.7)
            
            # Plot statistics for Tandil
            for stat in ['mean', 'median', 'max', 'min']:
                plt.plot(season_data.index, season_data[(stat, 'TANDIL AERO')],
                         label=f'Tandil {stat.capitalize()}', color=colors['TANDIL AERO'],
                         linestyle=line_styles[stat], alpha=0.7)
            
            # Plot temperature differences
            plt.plot(season_data.index, season_data[('mean_diff', '')],
                     label='Mean Difference', color=colors['temp_diff'],
                     linestyle='-', alpha=0.7)
            plt.plot(season_data.index, season_data[('median_diff', '')],
                     label='Median Difference', color=colors['temp_diff'],
                     linestyle='--', alpha=0.7)
            
            # Add statistics to the plot
            avg_diff = season_data[('mean_diff', '')].mean()
            max_diff = season_data[('mean_diff', '')].max()
            min_diff = season_data[('mean_diff', '')].min()
            
            stats_text = f'Avg Diff: {avg_diff:.1f}°C\nMax Diff: {max_diff:.1f}°C\nMin Diff: {min_diff:.1f}°C'
            plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.title(f'{season} Temperature Comparison: Buenos Aires vs Tandil ({date_range})')
            plt.xlabel('Hour of Day')
            plt.ylabel('Temperature (°C)')
            plt.xticks(range(0, 24, 2))
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)
            
            plt.tight_layout()
            output_file = f'plots/temperature_comparison_{season.lower()}.png'
            plt.savefig(output_file, bbox_inches='tight', dpi=300)
            plt.close()
            logger.info(f"Saved {season} plot to {output_file}")
            
            # Print seasonal statistics
            print(f"\n{season} Statistics:")
            print(f"Average temperature difference: {avg_diff:.2f}°C")
            print(f"Maximum difference: {max_diff:.2f}°C (at {season_data[('mean_diff', '')].idxmax()}:00)")
            print(f"Minimum difference: {min_diff:.2f}°C (at {season_data[('mean_diff', '')].idxmin()}:00)")
            print("\nHourly Temperatures and Differences:")
            print(pd.DataFrame({
                'Buenos Aires Mean': season_data[('mean', 'BUENOS AIRES OBSERVATORIO')].round(2),
                'Buenos Aires Median': season_data[('median', 'BUENOS AIRES OBSERVATORIO')].round(2),
                'Tandil Mean': season_data[('mean', 'TANDIL AERO')].round(2),
                'Tandil Median': season_data[('median', 'TANDIL AERO')].round(2),
                'Mean Difference': season_data[('mean_diff', '')].round(2),
                'Median Difference': season_data[('median_diff', '')].round(2)
            }))

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 