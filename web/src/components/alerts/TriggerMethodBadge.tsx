interface Props {
  method: string;
}

const colors: Record<string, string> = {
  GESTURE: '#8b5cf6', // Purple
  SHAKE: '#f59e0b',   // Yellow
  POWER_BUTTON: '#ef4444', // Red
  TIMEOUT: '#3b82f6',  // Blue
  MANUAL: '#6b7280',  // Gray
};

export default function TriggerMethodBadge({ method }: Props) {
  return (
    <span style={{
      backgroundColor: colors[method] || '#6b7280',
      color: 'white',
      padding: '4px 8px',
      borderRadius: '4px',
      fontSize: '12px',
      fontWeight: 'bold'
    }}>
      {method}
    </span>
  );
}