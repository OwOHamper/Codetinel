import { Table, TableHeader, TableRow, TableHead, TableCell, TableBody } from './ui/table';
import SeverityDisplay from './SeverityDipslay';
import React from 'react';
// import { Checkbox } from "@/components/ui/checkbox"; // Import Checkbox from ShadCN
import { Checkbox } from '@/components/ui/checkbox';

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
        {data.map((row, index) => (
          <TableRow key={row.name}>
            <TableCell className="w-1/2">{row.name}</TableCell>
            <TableCell><SeverityDisplay severity={row.severity} /></TableCell>
            <TableCell>{row.status}</TableCell>
            <TableCell className="w-1/100">
              <Checkbox
                checked={selectedRows.has(index)}
                onCheckedChange={() => handleRowSelection(index)}
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
