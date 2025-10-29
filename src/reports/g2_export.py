# Add to G2Exporter class

def export_hy3(self, times: List[LaneTiming], meet_info: Dict, filepath: str) -> bool:
    """
    Export to HY3 format (Hy-Tek Meet Manager)
    Format specs based on MM 8.0
    """
    try:
        with open(filepath, 'w') as f:
            # File header
            f.write("A1")
            f.write(f"{meet_info['meet_name']:<20}")
            f.write(datetime.now().strftime("%Y%m%d"))
            
            # Meet information
            f.write("D1")
            f.write(f"{meet_info['event_number']:>4}")
            f.write(f"{meet_info['event_gender']:1}")
            f.write(f"{meet_info['distance']:>4}")
            f.write(f"{meet_info['stroke']:>2}")
            f.write(f"{meet_info['round']:1}")
            
            # Results
            for time in times:
                f.write("D2")
                f.write(f"{time.lane:>2}")
                f.write(f"{self._format_time_hy3(time.time):>8}")
                f.write(f"{time.status:2}")
                
                # Splits
                if time.splits:
                    f.write("D3")
                    for split in time.splits:
                        f.write(f"{self._format_time_hy3(split):>8}")
            
            return True
    except Exception as e:
        self.logger.error(f"HY3 export failed: {e}")
        return False

def export_cl2(self, times: List[LaneTiming], meet_info: Dict, filepath: str) -> bool:
    """
    Export to CL2 format (Colorado Time Systems)
    """
    try:
        with open(filepath, 'w') as f:
            # Header
            f.write("2CL")
            f.write(datetime.now().strftime("%Y%m%d%H%M%S"))
            
            # Meet data
            f.write(f"M1,{meet_info['meet_name']}\n")
            f.write(f"E1,{meet_info['event_number']},{meet_info['event_name']}\n")
            
            # Times
            for time in times:
                # Main time
                f.write(f"T1,{time.lane},{self._format_time_cl2(time.time)}\n")
                
                # Splits
                if time.splits:
                    split_data = ",".join(self._format_time_cl2(s) for s in time.splits)
                    f.write(f"S1,{time.lane},{split_data}\n")
                
                # Backup times
                if time.backup_times:
                    backup_data = ",".join(self._format_time_cl2(t) for t in time.backup_times)
                    f.write(f"B1,{time.lane},{backup_data}\n")
                
                # Reaction time
                if time.reaction_time is not None:
                    f.write(f"R1,{time.lane},{time.reaction_time:.3f}\n")
            
            return True
    except Exception as e:
        self.logger.error(f"CL2 export failed: {e}")
        return False

def _format_time_hy3(self, time: float) -> str:
    """Format time for HY3 format"""
    minutes = int(time // 60)
    seconds = time % 60
    return f"{minutes:02d}{seconds:05.2f}"

def _format_time_cl2(self, time: float) -> str:
    """Format time for CL2 format"""
    return f"{time:.3f}"
