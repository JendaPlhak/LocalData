package com.wth.localinfo.jdbc;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import com.wth.localinfo.model.MappedParams;

/**
 * Reads database stored data and maps them based on provided header.
 */
public class JDBCReader {

    private final String[] mTableHeader;

    /** Table for loading data after transformation. */
    private final static String TRANSFORMATION_TABLE_NAME = "whatTheHack";

    public JDBCReader(String[] mTableHeader) {
        super();
        this.mTableHeader = mTableHeader;
    }

    public String[] loadHeader() throws IOException {
        Connection conn = jdbcInit();
        Statement stmt = null;
        ResultSet rs = null;
        String[] header = null;
        try {
            stmt = conn.createStatement();
            rs = selectAllQuery(stmt, 1);
            ResultSetMetaData resultMetaData = rs.getMetaData();
            int columnCount = resultMetaData.getColumnCount();
            header = new String[columnCount];
            for (int columnIndex = 1; columnIndex <= columnCount; columnIndex++) {
                int arrayIndex = columnIndex-1;
                header[arrayIndex] = resultMetaData.getColumnName(columnIndex);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            closeQuietly(rs);
            closeQuietly(stmt);
            closeQuietly(conn);
        }
        return header;
    }

    public List<MappedParams> load(int limit) {
        List<MappedParams> mappedRows = new ArrayList<MappedParams>();
        Connection conn = jdbcInit();
        Statement stmt = null;
        ResultSet rs = null;
        try {
            stmt = conn.createStatement();
            rs = selectAllQuery(stmt, limit);
            while (rs.next()) {
                MappedParams params = new MappedParams();
                for (String column : mTableHeader) {
                    String rowValue = rs.getString(column);
                    params.put(column, rowValue);
                }
                mappedRows.add(params);
            }
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } finally {
            closeQuietly(rs);
            closeQuietly(stmt);
            closeQuietly(conn);
        }
        return mappedRows;
    }

    private ResultSet selectAllQuery(Statement stmt, int limit) throws SQLException {
        String sql = "SELECT * FROM " + TRANSFORMATION_TABLE_NAME + " limit " + limit;
        System.out.println(sql);
        return stmt.executeQuery(sql);
    }

    private Connection jdbcInit() {
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
            return null;
        }

        Connection conn = null;
        try {
            conn = DriverManager.getConnection("jdbc:mysql://sh-tapi.keboola.com:3306/sand_662_53090?useUnicode=true&amp;amp;characterEncoding=UTF-8", "user_991",
                    "eK2bH8nK6vW3uK5j");

        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }

        if (conn == null) {
            System.out.println("Failed to make connection!");
            return null;
        }
        return conn;
    }

    private void closeQuietly(AutoCloseable closeable) {
        try {
            if (closeable != null) {
                closeable.close();
            }
        } catch (Exception se) {
            se.printStackTrace();
        }
    }
}
