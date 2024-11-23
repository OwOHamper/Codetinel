import { Table, TableHeader, TableRow, TableHead, TableCell, TableBody } from './ui/table'
import React from 'react'


interface DataRow {
  name: string;
  severity: string;
  status: string;
}

interface TableProps {
  data: DataRow[];
}

export default function VulnerabilitiesTable({ data }: TableProps) {
  return (
    <Table className="border">
      <TableHeader className="display-sticky">
        <TableRow>
          <TableHead className="text-center">Name</TableHead>
          <TableHead className="text-center">Severity</TableHead>
          <TableHead className="text-center">Status</TableHead>
          <TableHead className="text-center">Checkbox</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((row) => (
          <TableRow className="text-center" key={row.name}>
            <TableCell>{row.name}</TableCell>
            <TableCell>{row.severity}</TableCell>
            <TableCell>{row.status}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
