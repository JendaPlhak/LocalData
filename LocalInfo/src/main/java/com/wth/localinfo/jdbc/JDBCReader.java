package com.wth.localinfo.jdbc;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.wth.localinfo.Utils;

/**
 * Reads database stored data and maps them based on provided header.
 */
public class JDBCReader {

    private final String[] mTableHeader;

    public JDBCReader(String[] mTableHeader) {
        super();
        this.mTableHeader = mTableHeader;
    }

    public List<Map<String, String>> load(int limit) {
        List<Map<String, String>> mappedRows = new ArrayList<Map<String, String>>();
        Connection conn = jdbcInit();
        Statement stmt = null;
        try {
            stmt = conn.createStatement();

            String columns = Utils.getItems(mTableHeader);
            String sql = "SELECT " + columns + " FROM whatTheHack limit "+limit;

            System.out.println(sql);
            ResultSet rs = stmt.executeQuery(sql);
            while (rs.next()) {
                Map<String, String> params = new HashMap<String, String>();
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
            conn = DriverManager.getConnection("jdbc:mysql://sh-tapi.keboola.com:3306/sand_662_53090", "user_991",
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
