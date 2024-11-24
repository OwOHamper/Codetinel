import { Table, TableHeader, TableRow, TableHead, TableCell, TableBody } from '@/components/ui/table';
import SeverityDisplay from '@/components/SeverityDipslay';
import StatusDisplay from '@/components/StatusDisplay';
import React from 'react';
import { Checkbox } from '@/components/ui/checkbox';
import { useNavigate } from 'react-router-dom';

interface DataRow {
  id: number;
  cve?: string;
  cwe?: string;
  severity: string;
  status: string;
}

interface TableProps {
  data: DataRow[];
}

export default function VulnerabilitiesTable({ data, selectedRows, setSelectedRows }: TableProps) {
  const [selectAll, setSelectAll] = React.useState(false);
  const navigate = useNavigate()

  // Toggle all rows
  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedRows([]);
    } else {
      const allIds = data.map(item => item.id);
      setSelectedRows(allIds);
    }
    setSelectAll(!selectAll);
  };

  // Toggle single row selection
  const handleRowSelection = (id: number) => {
    setSelectedRows(prevSelectedRows => {
      if (prevSelectedRows.includes(id)) {
        return prevSelectedRows.filter(rowId => rowId !== id);
      } else {
        return [...prevSelectedRows, id];
      }
    });
  };

  // Check if all rows are selected
  const isAllSelected = selectedRows.length === data.length;

  return (
    <Table className="border">
      <TableHeader className="top-0 sticky bg-gray-200">
        <TableRow>
          <TableHead >Name</TableHead>
          <TableHead>File key</TableHead>
          <TableHead>Severity</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>
            <Checkbox
              className="mr-2"
              checked={isAllSelected}
              onCheckedChange={handleSelectAll}
            />
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((item) => (
          <TableRow key={item.id} className="cursor-pointer" onClick={() => navigate(`./error/${item.id}`)}>
            <TableCell>{item.cve || item.cwe}</TableCell>
            <TableCell>
              {item.file_key && (
                <div className="inline-flex text-xs bg-gray-200 rounded-md px-2 p-1">
                  {item.file_key}
                </div>
              )}
            </TableCell>
            <TableCell>
              <SeverityDisplay severity={item.severity} />
            </TableCell>
            <TableCell>
              <StatusDisplay status={item.status} />
            </TableCell>
            <TableCell onClick={(e) => e.stopPropagation()}>
              <Checkbox
                className="mr-2"
                checked={selectedRows.includes(item.id)}
                onCheckedChange={() => handleRowSelection(item.id)}
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
