import { Table, TableHeader, TableRow, TableHead, TableCell, TableBody } from '@/components/ui/table';
import SeverityDisplay from '@/components/SeverityDipslay';
import StatusDisplay from '@/components/StatusDisplay';
import React from 'react';
import { Checkbox } from '@/components/ui/checkbox';
import { useNavigate } from 'react-router-dom';

interface DataRow {
  name: string;
  severity: string;
  status: string;
}

interface TableProps {
  data: DataRow[];
}

export default function VulnerabilitiesTable({ data }: TableProps) {
  const [selectedRows, setSelectedRows] = React.useState<Set<number>>(new Set()); // Track selected row indices
  const [selectAll, setSelectAll] = React.useState(false); // Track whether all rows are selected
  const navigate = useNavigate()

  // Toggle all rows
  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedRows(new Set()); // Deselect all
    } else {
      const allIndices = new Set(data.map((_, index) => index)); // Select all using indices
      setSelectedRows(allIndices);
    }
    setSelectAll(!selectAll);
  };

  // Toggle single row selection
  const handleRowSelection = (index: number) => {
    setSelectedRows((prevSelectedRows) => {
      const newSelectedRows = new Set(prevSelectedRows);
      if (newSelectedRows.has(index)) {
        newSelectedRows.delete(index); // Deselect the row
      } else {
        newSelectedRows.add(index); // Select the row
      }
      return newSelectedRows;
    });
  };

  // Check if all rows are selected
  const isAllSelected = selectedRows.size === data.length;

  return (
    <Table className="border">
      <TableHeader className="top-0 sticky bg-gray-200">
        <TableRow>
          <TableHead >Name</TableHead>
          <TableHead>Severity</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>
            <Checkbox
              checked={isAllSelected}
              onCheckedChange={handleSelectAll}
            />
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((item) => (
          <TableRow key={item.id} className="cursor-pointer" onClick={() => navigate(`./error/${item.id}`)}>
            <TableCell className="w-1/2">{item.cve || item.cwe}</TableCell>
            <TableCell>
              <SeverityDisplay severity={item.severity} />
            </TableCell>
            <TableCell>
              <StatusDisplay status={item.status} />
            </TableCell>
            <TableCell className="w-1/100" onClick={(e) => e.stopPropagation()}>
              <Checkbox
                checked={selectedRows.has(item.id)}
                onCheckedChange={() => handleRowSelection(item.id)}
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
