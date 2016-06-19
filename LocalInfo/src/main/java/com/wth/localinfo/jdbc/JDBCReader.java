package com.wth.localinfo.jdbc;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
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

    public List<MappedParams> load(int limit) {
        List<MappedParams> mappedRows = new ArrayList<MappedParams>();
        Connection conn = jdbcInit();
        Statement stmt = null;
        try {
            stmt = conn.createStatement();

            String sql = "SELECT * FROM " + TRANSFORMATION_TABLE_NAME + " limit " + limit;

            System.out.println(sql);
            ResultSet rs = stmt.executeQuery(sql);
            while (rs.next()) {
                MappedParams params = new MappedParams();
                for (String column : mTableHeader) {
                    String rowValue = rs.getString(column);
                    params.put(column, rowValue);
                }
                mappedRows.add(params);
            }
            rs.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } finally {
            closeQuietly(stmt);
            closeQuietly(conn);
        }
        return mappedRows;
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
